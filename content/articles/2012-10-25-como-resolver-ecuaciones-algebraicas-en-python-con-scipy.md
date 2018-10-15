---
title: Cómo resolver ecuaciones algebraicas en Python con SciPy
date: 2012-10-25T15:07:59+00:00
author: Juan Luis Cano
slug: como-resolver-ecuaciones-algebraicas-en-python-con-scipy
tags: ecuaciones no lineales, python, scipy, scipy.optimize

## Introducción

En este artículo vamos a utilizar las rutinas de búsqueda de raíces ya disponibles en el módulo [`scipy.optimize`](http://docs.scipy.org/doc/scipy/reference/optimize.html#root-finding) para **resolver ecuaciones algebraicas con Python**. Ya vimos hace tiempo [cómo encontrar el mínimo de una función con SciPy](https://pybonacci.org/2012/03/28/como-encontrar-el-minimo-de-una-funcion-usando-scipy/ "¿Cómo encontrar el mínimo de una función usando scipy?"), y también [cómo implementar los métodos de la bisección y de Newton en Python](https://pybonacci.org/2012/04/18/ecuaciones-no-lineales-metodo-de-biseccion-y-metodo-de-newton-en-python/ "Ecuaciones no lineales: método de bisección y método de Newton en Python"). Ahora, además, exploraremos el caso de **sistemas de ecuaciones**.

_**En esta entrada se ha usado python 2.7.3, numpy 1.6.2 y scipy 0.11.**_

## Ejemplo básico: métodos de Brent y de Newton

Aunque el método de la bisección es muy conocido porque conceptualmente es muy sencillo de entender, nos vamos a olvidar de él y vamos a utilizar en su lugar el **método de Brent**, que viene implementado en SciPy en la función [`scipy.optimize.brentq`](http://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.brentq.html), ya que [según la documentación](http://docs.scipy.org/doc/scipy/reference/tutorial/optimize.html#scalar-functions) es la mejor opción. El [método de Brent](http://en.wikipedia.org/wiki/Brent%27s_method) es un algoritmo complicado que combina el método de la bisección, el de la secante e interpolación cuadrática inversa: como el método de la bisección, tiene convergencia garantizada siempre que demos un intervalo $[a, b]$ donde $f(a) f(b) < 0$; es decir, que haya un cambio de signo en el intervalo.

<!--more-->

En el caso en que conozcamos un valor próximo a la solución, seguiremos utilizando el método de Newton o el de la secante a través de la función [`scipy.optimize.newton`](http://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.newton.html), que selecciona uno u otro en el caso de que le pasemos la función derivada o no. Vamos a resolver este ejemplo que me acabo de inventar:

<p style="text-align:center">
  $\displaystyle e^{x / 3} \cos{x} + 10 \sin{3 x} = x^2 / 4$
</p>

    :::python
    import numpy as np
    import matplotlib.pyplot as plt
    x = np.linspace(0, 9, 100)
    plt.plot(x, exp(x / 3) * cos(x) + 10 * sin(3 * x), x, x ** 2 / 4)

![Ecuación 1](https://pybonacci.org/images/2012/10/ecuacion1.png)

Antes que nada debemos definir la función que va a representar la ecuación. Todas las subrutinas de búsqueda de raíces en realidad buscan ceros de funciones, así que debemos escribir

$f(x) \equiv \displaystyle e^{x / 3} \cos{x} + 10 \sin{3 x} - x^2 / 4 = 0$

    :::python
    def f(x):
        """Ecuación no lineal.
        Asume que se ha importado NumPy de la forma
          import numpy as np
        """
        return np.exp(x / 3.0) * np.cos(x) + 10 * np.sin(3 * x) - x ** 2 / 4

Vamos a buscar primero la solución que vemos que está entre 4 y 5. Para ello, utilizamos el método de Brent:

    :::python
    from scipy.optimize import brentq
    sol1 = brentq(f, 4.0, 5.0)
    print sol1  # 4.40989799172

Sencillo, ¿no? Ahora si queremos buscar la solución que está cerca de 2, podemos probar el método de la secante:

    :::python
    from scipy.optimize import newton
    sol2 = newton(f, 2.0)
    print sol2  # 2.17349784856

Más sencillo todavía 😉 estas son las dos soluciones:<figure id="attachment_1088" style="width: 374px" class="wp-caption aligncenter">

![Soluciones de la ecuación 1](https://pybonacci.org/images/2012/10/ecuacion1_soluciones.png)

<p style="text-align:center">
  <h2>
    Aplicación: funciones implícitas
  </h2>
  
  <p>
    Podemos utilizar estos métodos de búsqueda de raíces de ecuaciones algebraicas para <strong>representar funciones implícitas</strong>. Mientras que las funciones explícitas vienen dadas de la forma $y = f(x)$, las implícitas están expresadas como $F(x, y) = 0$, de tal forma que no es posible «despejar» una variable en función de la otra. Sin embargo, podemos obtener una representación siguiendo el siguiente método:
  </p>
  
  <ol>
    <li>
      Discretizamos el intervalo $[x_0, x_{N - 1}]$ en $N$ elementos.
    </li>
    <li>
      Para cada valor $\tilde{x}_i$ con $i \in 0, ..., N - 1$ resolvemos la ecuación $F(\tilde{x}_i, y) = 0$ y almacenamos la solución en $y_i$.
    </li>
    <li>
      Proseguimos hasta que tengamos la lista de valores $y_0, y_1, ..., y_{N - 1}$.
    </li>
  </ol>
  
  <p>
    Lo bueno de este algoritmo es que, una vez dado el primer paso, para el siguiente tenemos un valor muy cerca de la solución, por lo que podemos usar métodos de convergencia rápida como el de Newton.
  </p>
  
  <p>
    Vamos a tomar un ejemplo con el que me encontré el otro día mientras estudiaba Aerotermodinámica. Tenemos una tobera cuya área transversal viene definida, en función de la coordenada &#040;x&#041; sobre el eje, por
  </p>
  
  <p>
    $A(x) = \begin{cases} 2 x^3 - 3 x^2 + 2 & 0 \leq x \le 1 &#092;\ -\frac{3}{8} x^3 + \frac{9}{4} x^2 - \frac{27}{8} x + \frac{5}{2} & 1 \leq x \le 3 \end{cases}$
  </p>
  
  <p>
    y que tiene esta pinta:
  </p>
  
    :::python
    x = np.linspace(0, 3, 151)
    def A(x):
        """Área transversal de la tobera.
    
        """
        def A1(x):
            return 2.0 * x ** 3 - 3.0 * x ** 2 + 2.0
    
        def A2(x):
            return -3.0 * x ** 3 / 8.0 + 9.0 * x ** 2 / 4.0 - 27.0 * x / 8.0 + 5.0 / 2.0
    
        return np.piecewise(x, [(0.0 &lt;= x) & (x &lt; 1.0), (1.0 &lt;= x) & (x &lt;= 3.0)], [A1, A2])
    
    plt.fill_between(x, np.sqrt(A(x) / np.pi), -np.sqrt(A(x) / np.pi), facecolor="#eebb22")
    plt.xlim((0, 3))
    plt.title("Tobera")
    plt.xlabel("x (m)")
    plt.ylabel("Radio (dm)")

    <p>
        <a href="https://pybonacci.org/images/2012/10/tobera.png"><img class="aligncenter size-full wp-image-1089" title="Tobera" alt="" src="https://pybonacci.org/images/2012/10/tobera.png" height="279" width="397" srcset="https://pybonacci.org/wp-content/uploads/2012/10/tobera.png 397w, https://pybonacci.org/wp-content/uploads/2012/10/tobera-300x210.png 300w" sizes="(max-width: 397px) 100vw, 397px" /></a>
      </p>
      
      <p>
        <strong>Nota</strong>: Recuerda que puedes leer en Pybonacci <a href="https://pybonacci.org/2012/10/10/funciones-definidas-a-trozos-con-arrays-de-numpy/">cómo definir funciones definidas a trozos en NumPy</a>.
      </p>
      
      <p>
        Y quiero conocer la distribución del número de Mach $M$ a lo largo de la misma, utilizando la ecuación
      </p>
      
      <p>
        $\displaystyle \frac{A(x)}{A^*} = \frac{1}{M(x)} \left( \frac{2}{1 + \gamma} \left( 1 + \frac{\gamma - 1}{2} M(x)^2 \right) \right)^{\frac{\gamma + 1}{2 (\gamma - 1)}}$
      </p>
      
      <p>
        donde $A^*$ es el área crítica y $\gamma = 1.4$ para el caso del aire. Date cuenta de que es imposible despejar $x$ en función de $M$ o viceversa, de tal forma que tenemos que resolver la relación implícita que existe entre estas variables. Este es el código:
    </p>

    :::python
    from scipy.optimize import brentq, newton
    def rel(M, gamma=1.4):
        """Parte derecha de la relación entre el número de Mach $M$
        y la relación de áreas $A / A^*$.
        """
        return (2 * (1 + (gamma - 1) * M ** 2 / 2) / (gamma + 1)) ** ((gamma + 1) / 2 / (gamma - 1)) / M
    def eq(M, A):
        """Función implícita entre el número de Mach y la relación
        de áreas.
        """
        return rel(M) - A
    # Para cada valor de x resolvemos la ecuación en M
    M = np.empty_like(x)
    # El primer paso lo damos con el método de Brent
    M[0] = brentq(eq, 0.001, 1, args=(A(x[0:1]),))
    # Comenzamos a iterar
    for i in xrange(1, len(x)):
        # El valor inicial para el método de Newton es la solución del
        # paso anterior
        M[i] = newton(eq, M[i - 1], args=(A(x[i - 1:i]),))
    # Representamos la solución
    plt.plot(x, M)
    plt.plot(x, np.ones_like(x), 'k--')
    plt.title(u"Distribución de $M$ a lo largo del eje de la tobera")
    plt.ylabel("M")
    plt.xlabel("x (m)")
    plt.annotate(s=u"Garganta", xy=(1.0, 1.0), xytext=(0.5, 1.6), arrowprops=dict(arrowstyle = "-&gt;"))

  <p>
    <a href="https://pybonacci.org/images/2012/10/distribucion_mach.png"><img class="aligncenter size-full wp-image-1087" title="Distribución número de Mach" alt="" src="https://pybonacci.org/images/2012/10/distribucion_mach.png" height="281" width="388" srcset="https://pybonacci.org/wp-content/uploads/2012/10/distribucion_mach.png 388w, https://pybonacci.org/wp-content/uploads/2012/10/distribucion_mach-300x217.png 300w" sizes="(max-width: 388px) 100vw, 388px" /></a>
  </p>
  
  <p>
    Otra cosa buena de este método es que, en relalidad, este tipo de funciones implícitas definen curvas con más de una «rama», pero físicamente para la solución de nuestro problema solo una suele ser la correcta, como es este caso. Si resolvemos la ecuación de esta manera podemos solucionar la rama que nos interesa.
  </p>
  
  <h2>
    Sistemas de ecuaciones no lineales
  </h2>
  
  <p>
    Si estamos en el caso de tener un sistema de ecuaciones no lineales, SciPy también tiene métodos para resolverlos, a través del paquete MINPACK. Utilizaremos la función <a href="http://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.root.html"><code>root</code></a>, que además soporta varios métodos de resolución en función de si proporcionamos el jacobiano del sistema o no.
  </p>
  
  <p>
    Vamos a resolver este ejemplo extraído de la documentación de SciPy:
  </p>
  
  <p>
    $\begin{cases} x \cos{y} & = 4 &#092;\ x y - y & = 5 \end{cases}$
  </p>
  
  <p>
    Una vez más, tenemos que transformar este sistema en $\vec{f}(\vec{x}) = \vec{0}$, donde las flechas indican vectores. En este caso,
  </p>
  
  <p>
    $\vec{x} = \begin{pmatrix} x &#092;\ y \end{pmatrix}$
  </p>
  
  <p>
    $\vec{f}(\vec{x}) \equiv \begin{pmatrix} x \cos{y} - 4 &#092;\ x y - y - 5 \end{pmatrix} = \vec{0}$
  </p>
  
  <p>
    El código en Python será:
  </p>
  
    :::python
    from scipy.optimize import root
    def f(x):
        """Sistema de dos ecuaciones con dos incógnitas.
        """
        return [
            x[0] * np.cos(x[1]) - 4,
            x[1]*x[0] - x[1] - 5
        ]
    sol = root(f, [1, 1], jac=False)  # Devuelve objecto Result
    print sol.x  # Result.x contiene la solución

  <p>
    Y esto ha sido todo, no olvides hacernos llegar tus sugerencias y comentarios. ¡Un saludo!
  </p>
