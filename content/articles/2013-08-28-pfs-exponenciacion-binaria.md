---
title: PFS: Exponenciación binaria
date: 2013-08-28T16:42:13+00:00
author: Kiko Correoso
slug: pfs-exponenciacion-binaria
tags: exponenciación binaria, optimización, PFS, potencias, python, Python fuente de sabiduria

Hoy voy a iniciar una serie nueva de entradas que se llamará '**p**ython, **f**uente de **s**abiduría' (PFS para abreviar). ¿Qué pretende esta serie? La idea básica es mostrar la influencia y realimentación entre las matemáticas y la programación. La idea e inspiración para estas entradas salió después de leer esta <a href="http://ch3m4.org/blog/2013/08/14/estudio-funcion-factorial-numpy/" target="_blank">entrada</a>.

Inauguraremos esta entrada con una forma de calcular la potencia entera de un número entero. Si tuviera que crear una función que calculase esto, la primera idea que se me ocurre es usar la fuerza bruta (soy así de primario)...

<pre><code class="language-python">def pow_fuerzabruta(x,n):
    y = x
    for i in range(1,n):
        y = y * x
    return y</code></pre>

Con la anterior función, la cual no he pensado mucho, lo que estamos haciendo son `n-1` multiplicaciones. A medida que aumente el exponente aumentará el tiempo de cálculo. Veámoslo en una gráfica:

<pre><code class="language-python">from matplotlib import pyplot as plt
n = [5, 25, 100, 1000, 10000, 100000]       # exponente
t = [1.13, 3.93, 17.8, 330, 15000, 1260000] # t en microsegundos
plt.xscale('log')
plt.yscale('log')
plt.plot(n,t)
plt.xlabel('valor del exponente n')
plt.ylabel('t en microsegundos')</code></pre>

[<img class="aligncenter size-full wp-image-1866" alt="pow_bruto" src="http://pybonacci.org/wp-content/uploads/2013/08/pow_bruto.png" width="396" height="278" srcset="https://pybonacci.org/wp-content/uploads/2013/08/pow_bruto.png 396w, https://pybonacci.org/wp-content/uploads/2013/08/pow_bruto-300x210.png 300w" sizes="(max-width: 396px) 100vw, 396px" />](http://pybonacci.org/wp-content/uploads/2013/08/pow_bruto.png)

[Nota: la escala de los ejes en la anterior figura es logarítmica]

Esto, cuando usamos números muy grandes, no es muy deseable. Por ello, vamos a mostrar el algortimo de hoy, la exponenciación binaria, también llamado algoritmo de izquierda a derecha binario, que nos permitirá reducir de forma drástica el número de operaciones a realizar. Su uso en Python lo podéis ver, por ejemplo, en la siguiente implementación de <a href="http://svn.python.org/view/python/tags/r271/Objects/longobject.c?view=markup" target="_blank"><code>long_pow</code></a> (ver a partir de línea 3376).

Podemos pensar que estas cosas son muy modernas y sofisticadas pero, en este caso, no es así. Los primeros orígenes de esta implementación para calcular potencias parece que sería anterior a 2200 años atrás. Según el libro de [Donald Knuth titulado _Seminumerical Algorithms, volume 2 of The Art of Computer Programming_, página 441](http://www.goodreads.com/book/show/112246.Art_of_Computer_Programming_Volume_2), podemos leer:

> El método es bastante antiguo; apareció antes del año 200 A.C. en _Pingala's Hindu classic Chandah-sutra_ [ver B. Datta y A.N. Singh, _History of Hindu Mathematics 1_, 1935]; sin embargo, parece que existen otras referencias a este método fuera de la India a lo largo de los 1000 años posteriores. Una discusión muy clara sobre como calcular `2n` de forma eficiente para valores de `n` arbitrarios sería debida a al-Uqlidisi de Damscus en 952 D.C.; podéis ver _The Arithmetic of al-Uglidisi_ por A.S. Saidan (1975), p. 341-342, donde las ideas generales están ilustradas para el caso de n=51. Ver también _al-Biruni's Chronology of Ancient Nations (1879)_, p. 132-136; durante el siglo XI, los avances del mundo árabe tuvieron una gran influencia.

Más información histórica sobre los orígenes la podéis encontrar en este <a href="http://arxiv.org/abs/math/0703658" target="_blank">artículo</a>.

Vamos a ver como funciona, más o menos, este algoritmo. La idea básica detrás del mismo es la siguiente (ver <a href="http://es.wikipedia.org/wiki/Exponenciaci%C3%B3n_binaria" target="_blank">wikipedia</a> para una explicación más completa):

Las potencias más rápidas de calcular son las que tienen la siguiente forma ${x^2}^n$. Estos es debido a que se pueden encontrar las potencias calculando el cuadrado del número de forma repetida.

Vamos a explicar el mismo ejemplo que al-Uqlidisi de Damscus (unos diez siglos más tarde...) considerando un número elevado a 51. Por tanto, puedo calcular $5^2$ con solo una multiplicación, $5^4={5^2}^2$ con solo dos multiplicaciones, $5^8={{5^2}^2}^2$ en tres multiplicaciones,...

Creo que vais viendo por donde van los tiros. El algoritmo explicado de forma muy básica sería para el ejemplo $5^{51}$:

  * Obtener el exponente como suma de potencias de 2

<p style="text-align:center;">
  En este caso sería 51 = 32 + 16 + 2 + 1
</p>

  * Encontrar la base de potencias de dos que aparecen en el exponente

<p style="text-align:center;">
  $5^1=5$
</p>

<p style="text-align:center;">
  $5^2 = 5 cdot 5 = 25$
</p>

<p style="text-align:center;">
  $5^4= 25 cdot 25 = 625$
</p>

<p style="text-align:center;">
  $5^8= 625 cdot 625 = 390625$
</p>

<p style="text-align:center;">
  $5^{16} = 390625 cdot 390625 = 152587890625$
</p>

<p style="text-align:center;">
  $5^{32} = 152587890625 cdot 152587890625 = 23283064365386962890625$
</p>

  * Y, por último, se multiplicarían de forma conjunta las potencias ya encontradas

<p style="text-align:center;">
  $5^{51} = 5^{32} cdot 5^{16} cdot 5^2 cdot 5 = 444089209850062616169452667236328125$
</p>

De esta forma, en lugar de multiplicar 5 por si mismo 50 veces solo hemos de realizar 8 multiplicaciones.

El que vamos a implementar es un algoritmo de exponenciación binaria pero de derecha a izquierda. Podéis ver los detalles en la <a href="http://en.wikipedia.org/wiki/Modular_exponentiation#Right-to-left_binary_method" target="_blank">wikipedia</a>.

<pre><code class="language-python">def my_pow(x,n):
    r = 1
    y = x
    while n &gt; 1:
        if n%2:
            r = r * y
        n = int(n/2)
        y = y * y
    r = r*y
    return r</code></pre>

Si calculamos los tiempos que hemos obtenido con la nueva función (`my_pow`) y los comparamos con la anterior implementación (`pow_fuerzabruta`) veremos la ganancia que hemos obtenido:

<pre><code class="language-python">from matplotlib import pyplot as plt
n = [5, 25, 100, 1000, 10000, 100000]       # exponente
t_bruta = [1.13, 3.93, 17.8, 330, 15000, 1260000] # t  para la primera función
t_bin = [1.34, 2.52, 3.68, 19.8, 765, 32800] # t para la segunda función
plt.plot(n,t_bruta, label='bruta')
plt.plot(n,t_bin, label='bin')
plt.legend()
plt.xlabel('valor del exponente n')
plt.ylabel('t en microsegundos')</code></pre>

[<img class="aligncenter size-full wp-image-1867" alt="pow_bruto_bin" src="http://pybonacci.org/wp-content/uploads/2013/08/pow_bruto_bin.png" width="429" height="268" srcset="https://pybonacci.org/wp-content/uploads/2013/08/pow_bruto_bin.png 429w, https://pybonacci.org/wp-content/uploads/2013/08/pow_bruto_bin-300x187.png 300w" sizes="(max-width: 429px) 100vw, 429px" />](http://pybonacci.org/wp-content/uploads/2013/08/pow_bruto_bin.png)

[Nota: Ahora, las escalas de los ejes son lineales]

Vemos que la ganancia, dependiendo del valor del exponente, es cada vez más importante a medida que aumenta el valor del mismo.

<pre><code class="language-python">for i, t1, t2 in zip(n, t_bruta, t_bin):
    print('Ganancia para n = {0:&gt;6}, {1:&gt;10.2f}'.format(i, t1/t2))</code></pre>

`<br />
Ganancia para n = 5, 0.84<br />
Ganancia para n = 25, 1.56<br />
Ganancia para n = 100, 4.84<br />
Ganancia para n = 1000, 16.67<br />
Ganancia para n = 10000, 19.00<br />
Ganancia para n = 100000, 38.00<br />
` 

Para números pequeños vemos que incluso puede llegar a ser peor pero para números grandes la ganancia es significativa llegando a valores en torno a 40 para un número `n` de orden $10^5$

Por último, solo comentar que las funciones \`pow\` y \`math.pow\` son más eficientes que lo que he hecho [(programadas en C)](http://hg.python.org/cpython/file/41de6f0e62fd/Modules/mathmodule.c). La idea de la entrada solo es mostrar que, gracias al trabajo y saber colectivo, la inteligencia que se esconde en las tripas de Python (y el resto de lenguajes de programación) es mucha y en el día a día ni nos damos cuenta de ello.

P.D.: Las funciones implementadas no contemplan exponentes negativos ni 0. He intentado simplificar el código al máximo para que se vea el bosque en lugar de los árboles.

Esta entrada la puedes descargar en formato notebook desde [nuestro repositorio en github](https://github.com/Pybonacci/notebooks).