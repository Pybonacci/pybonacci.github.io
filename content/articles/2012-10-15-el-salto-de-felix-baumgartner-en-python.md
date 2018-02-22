---
title: El salto de Felix Baumgartner en Python
date: 2012-10-15T17:40:29+00:00
author: Juan Luis Cano
slug: el-salto-de-felix-baumgartner-en-python
tags: Baumgartner, EDOs, python, stratos

## Introducción

Supongo que todos estáis al tanto de la hazaña de [Felix Baumgartner](http://en.wikipedia.org/wiki/Felix_Baumgartner), el hombre que ha saltado desde una altura de más de 120000 pies desde un globo, convirtiéndose en el hombre que más alto ha saltado y el que ha alcanzado la mayor velocidad sin ayuda mecánica como parte de la [misión Red Bull Stratos](http://www.redbullstratos.com/).



En Pybonacci somos _tan_ frikis, que vamos a visualizar el salto supersónico de Baumgartner como mejor se nos da: con Python 😉

<!--more-->

**Nota**: Esto es un artículo recreativo que he escrito en un par de horas y he hecho unas cuantas suposiciones que no tienen porqué coincidir con la realidad. Tómese esto en cuenta a la hora de valorar los resultados.

## Formulación del problema

**Nota**: Esta es la parte aburrida. Las gráficas están más abajo 🙂

La ecuación diferencial que gobierna el movimiento en caída libre de Baumgartner es

<p style="text-align:center">
  $\displaystyle m \frac{d^2 y}{d t^2} = -m g + D$
</p>

donde el término $-m g$ corresponde a la **atracción gravitatoria** y $D$ es el **rozamiento aerodinámico**. La presencia de esta componente es fundamental, porque es la que determina la velocidad de equilibrio o **velocidad terminal** que se alcanza durante el salto. En los típicos problemas de escuela secundaria se desprecia, pero en Pybonacci hacemos las cosas con rigor 😉

El rozamiento aerodinámico tiene por expresión $D = \frac{1}{2} \rho v^2 C\_D A$, donde $C\_D$ y $A$ son respectivamente el coeficiente de rozamiento y un área de referencia y son parámetros que dependen del cuerpo que estemos estudiando. Vemos también que el rozamiento es proporcial al cuadrado de la velocidad, de tal forma que cuanto más rápido vaya el cuerpo, mayor será esta fuerza: por eso se alcanza una velocidad terminal.

Hay una cosa más que hay que tener en cuenta, y es que al ser el salto desde una altura tan grande, _la densidad del aire no puede considerarse constante_. ¿Qué significa esto? Que, una vez alcanzada la velocidad terminal, el rozamiento irá aumentando conforme pase el tiempo, aquella irá disminuyendo… y el cuerpo _caerá cada vez más despacio_.

«Ehm… ¿cada vez más despacio? Chicos de Pybonacci, dedicaos a Python porque la física se os da fatal». Eso pensáis, ¿eh? ¡ya veremos!

Para completar la formulación del problema nos falta saber el valor del coeficiente de rozamiento $C_D$, el área de referencia $A$ y la ley de variación de la densidad $\rho$ con la altitud. Para los dos primeros, [con el permiso de Arturo Quirantes Sierra](http://fisicadepelicula.blogspot.com.es/2012/10/la-fisica-del-salto-baumgartner.html), vamos a suponer que $C_D = 0.4$ y $A = 1.0~m^2$.

En cuanto a la densidad, vamos a acudir utilizar [el paquete AeroCalc](http://pypi.python.org/pypi/AeroCalc/), que nos permite, entre otras cosas, calcular propiedades de la atmósfera según el modelo de la Atmósfera Estándar Internacional de 1976 hasta 84.852 kilómetros.

¡Ya podemos resolver el problema! Para ello, vamos a hacer algo que no habíamos explicado todavía en el blog que es cómo resolver **ecuaciones diferenciales ordinarias** o EDOs en Python con SciPy, en concreto problemas de Cauchy o de valor inicial, como es este caso. Para ello utilizaremos la función `odeint` del paquete `scipy.integrate`. Si tenemos un sistema de EDOs del tipo

$\displaystyle \frac{d y}{d t} = f(y, t)$

la función `odeint` acepta, como mínimo, estos argumentos:

  * La función del sistema f(y, t0, ...), que a su vez recibe como argumentos el vector y y el instante de tiempot0.
  * El array y0 de condiciones iniciales en el instante t[0].
  * El array t de valores temporales para los que resolver el sistema de ecuaciones diferenciales. El primer valor debe ser el que corresponde al vector de condiciones iniciales y0.

Como vemos la forma del sistema dada más arriba no corresponde con la forma en la que tenemos nosotros expresada la ecuación: al ser una ecuación de segundo orden, hay que transformarla en un sistema de dos ecuaciones de primer orden. Para eso, definimos la variable

$v = \frac{d y}{d t}$

y el sistema queda de la siguiente manera:

<p style="text-align:center">
  $\displaystyle \frac{d}{d t} \begin{pmatrix} y \\ v \end{pmatrix} = \begin{pmatrix} v \\ -g - \frac{1}{2 m} \rho(y) v^2 C_D A \end{pmatrix}$
</p>

¡Ya podemos empezar a calcular!

## Caída libre

Este es el código del programa. Se explica por sí solo:

<pre><code class="language-python">import numpy as np
from scipy.integrate import odeint
from aerocalc import std_atm
def f(y, t0, rho, m, C_D, A):
    """Función del sistema.
    Procede de reducir de orden la ecuación
    $m frac{d^2 y}{d t^2} = -m g - frac{1}{2} rho v^2 C_D A$
    suponiendo gravedad constante igual a $g = 9.81 m s^{-2}$ y densidad
    función de la altitud $rho = rho(y)$.
    Parámetros
    ----------
    y : array_like
        Vector de variables $(y, dot{y})$.
    t0 : array_like
        Vector de valores temporales.
    rho : callable(y)
        Densidad en función de la altitud.
    m : float
        Masa del cuerpo.
    C_D : float
        Coeficiente de rozamiento.
    A : float
        Área de referencia
    """
    g = 9.8  # m
    return np.array([
        y[1],
        -g + rho(y[0]) * y[1] ** 2 * C_D * A / (2 * m)
    ])
# Datos iniciales
h0 = 39000.0  # m
C_D = 0.4
A = 1.0  # m^2
m = 80  # kg
def alt2dens(y):
    """Devuelve la densidad en función de la altitud con unidades de
    Sistema Internacional.
    """
    return std_atm.alt2density(y, alt_units='m', density_units='kg/m**3')
import matplotlib.pyplot as plt
t = np.linspace(0, 4 * 60)  # Cuatro minutos de caída libre
y0 = np.array([h0, 0])
sol = odeint(f, y0, t, args=(alt2dens, m, C_D, A))
y = sol[:, 0]
v = sol[:, 1]
fig = plt.figure()
fig.suptitle(u"Caída libre")
ax1 = fig.add_subplot(211)
ax1.plot(t, y)
ax1.set_ylabel('y (m)')
ax1.set_xlabel('t (s)')
ax2 = fig.add_subplot(212)
ax2.plot(t, -v * 3.6)  # km/h
ax2.set_ylabel('v (km / h)')
ax2.set_xlabel('t (s)')</code></pre><figure id="attachment_1037" style="width: 407px" class="wp-caption aligncenter">

[<img class="size-full wp-image-1037" title="Caída libre" alt="" src="http://new.pybonacci.org/images/2012/10/caida_libre2.png" height="410" width="407" srcset="https://pybonacci.org/wp-content/uploads/2012/10/caida_libre2.png 407w, https://pybonacci.org/wp-content/uploads/2012/10/caida_libre2-150x150.png 150w, https://pybonacci.org/wp-content/uploads/2012/10/caida_libre2-297x300.png 297w" sizes="(max-width: 407px) 100vw, 407px" />](http://new.pybonacci.org/images/2012/10/caida_libre2.png)<figcaption class="wp-caption-text">Altitud y velocidad de caída en función del tiempo</figcaption></figure> 

Ajá, ¿no os creíais que cada vez caía más despacio? 😛 Esto evidentemente tenía cierto truco, pero ¡ya se ven los resultados en las gráficas!

## La barrera del sonido

Y ahora la gran pregunta, ¿superó Baumgartner la barrera del sonido? Para saberlo, necesitamos saber, aparte de su velocidad real, la distribución de la velocidad del sonido en el aire, que no es constante al no serlo la temperatura. Con esto podemos calcular el **número de Mach**:

$\displaystyle M = \frac{u}{c}$

siendo $u$ la velocidad, $c = \sqrt{\gamma R T}$ la velocidad del sonido en el aire, $\gamma$ y $R$ dos parámetros de valores conocidos (la razón de calores específicos y la constante específica del aire) y $T$ la temperatura, que conocemos gracias al modelo de la Atmósfera Estándar Internacional. Veamos:

<pre><code class="language-python">gamma = 1.4
R = 287.0  # [SI]
c = np.empty_like(v)
for i in range(len(v)):
    c[i] = np.sqrt(gamma * R * std_atm.alt2temp(y[i], alt_units='m', temp_units='K'))
M = -v / c
plt.plot(t, M)
plt.plot(t, np.ones_like(t), 'k--')
plt.ylabel('M')
plt.xlabel('t (s)')</code></pre><figure id="attachment_1038" style="width: 389px" class="wp-caption aligncenter">

[<img class="size-full wp-image-1038" title="Número de Mach" alt="" src="http://new.pybonacci.org/images/2012/10/mach_number.png" height="268" width="389" srcset="https://pybonacci.org/wp-content/uploads/2012/10/mach_number.png 389w, https://pybonacci.org/wp-content/uploads/2012/10/mach_number-300x206.png 300w" sizes="(max-width: 389px) 100vw, 389px" />](http://new.pybonacci.org/images/2012/10/mach_number.png)<figcaption class="wp-caption-text">Número de Mach en función del tiempo</figcaption></figure> 

Así que sí, _¡Felix Baumgartner superó la barrera del sonido!_ Según Pybonacci, por supuesto 😉