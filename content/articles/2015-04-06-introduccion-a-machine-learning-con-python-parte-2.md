---
title: Introducción a Machine Learning con Python (Parte 2)
date: 2015-04-06T17:27:44+00:00
author: Pablo Fernández
slug: introduccion-a-machine-learning-con-python-parte-2
tags: machine learning, python, regresión lineal, regresión logística, scikit-learn

En la entrada anterior, [Introducción a Machine Learning con Python (Parte 1)](https://pybonacci.org/2015/01/14/introduccion-a-machine-learning-con-python-parte-1/ "Introducción a Machine Learning con Python (Parte 1)"), di unas pequeñas pinceladas sobre lo que es el Aprendizaje Automático con algunos ejemplos prácticos. Ahora vamos a adentrarnos en materia de un modo más estructurado viendo paso a paso algunas de las técnicas que podemos emplear en Python.

Podemos dividir los problemas de aprendizaje automático en dos grandes categorías (Pedregosa et al., 2011):

  * **Aprendizaje supervisado**, cuando el conjunto de datos viene con los atributos adicionales que queremos predecir. El problema puede clasificarse en dos categorías: 
      * Regresión: los valores de salida consisten en una o más variables continuas. Un ejemplo es la predicción del valor de una casa en función de su superficie útil, número de habitaciones, cuartos de baños, etc.
      * Clasificación: las muestras pertenecen a dos o más clases y queremos aprender a partir de lo que ya conocemos cómo clasificar nuevas muestras. Tenemos como ejemplo el _Iris dataset_ que ya mostramos en la entrada anterior
  * **Aprendizaje no supervisado**, cuando no hay un conocimiento a priori de las salidas que corresponden al conjunto de datos de entrada. En estos casos el objetivo es encontrar grupos mediante _<a title="Cluster analysis" href="https://en.wikipedia.org/wiki/Cluster_analysis" target="_blank">clustering</a>_ o determinar una distribución de probabilidad sobre un conjunto de entrada.

Como vemos, en ambos casos el aprendizaje automático trata de aprender una serie de propiedades del conjunto de datos y aplicarlos a nuevos datos.

Ésta entrada se la vamos a dedicar al aprendizaje supervisado, acompañando cada una de las técnica que veamos con un Notebook de [Jupyter](https://jupyter.org)

## Aprendizaje supervisado

Empezaremos por el principio, y lo más sencillo, que es ajustar los datos a una línea para pasar luego a ver diferentes modelos de clasificación en orden creciente de complejidad en subsiguientes entradas.

<!--more Sigue leyendo...-->

### <a href="http://nbviewer.ipython.org/github/pybonacci/notebooks/blob/master/Machine%20Learning/Regresión%20lineal.ipynb" target="_blank">Regresión lineal</a>

Los modelos lineales son fundamentales tanto en estadística como en el aprendizaje automático, pues muchos métodos se apoyan en la combinación lineal de variables que describen los datos. Lo más sencillo es ajustar una línea recta con `LinearRegression`.

Para mostrar cómo funcionan estos modelos vamos a emplear uno de los <a title="Dataset loading utilities" href="http://scikit-learn.org/stable/datasets/index.html" target="_blank">dataset</a> que ya incorpora scikit-learn.

    :::python
    from sklearn import datasets
    boston = datasets.load_boston()

El Boston dataset es un conjunto de datos para el análisis de los precios de las viviendas en la región de Boston. Con `boston.DESCR` podemos obtener una descripción del dataset, con información sobre el mismo, como el tipo de atributos.

    Boston House Prices dataset
    Notes
    ------
    Data Set Characteristics:   
        :Number of Instances: 506 
        :Number of Attributes: 13 numeric/categorical predictive
        :Median Value (attribute 14) is usually the target
        :Attribute Information (in order):
        - CRIM     per capita crime rate by town
        - ZN       proportion of residential land zoned for lots over 25,000 sq.ft.
        - INDUS    proportion of non-retail business acres per town
        - CHAS     Charles River dummy variable (= 1 if tract bounds river; 0 otherwise)
        - NOX      nitric oxides concentration (parts per 10  million)
        - RM       average number of rooms per dwelling
        - AGE      proportion of owner-occupied units built prior to 1940
        - DIS      weighted distances to five Boston employment centres
        - RAD      index  of accessibility to radial highways
        - TAX      full-value property-tax  rate per $10,000
        - PTRATIO  pupil-teacher ratio by town
        - B        1000(Bk - 0.63)^2 where Bk is the proportion of blacks by town
        - LSTAT    % lower status of the population
        - MEDV     Median value of owner-occupied homes in $1000's
        :Missing Attribute Values: None

Vemos que tenemos 506 muestras con 13 atributos que nos ayudarán a predecir el precio medio de la vivienda. Ahora bien, no todos los atributos serán significativos ni todos tendrán el mismo peso a la hora de determinar el precio de la vivienda; pero eso es algo que iremos viendo conforme adquiramos experiencia e intuición.

Ya tenemos los datos, vamos a ajustar una línea recta para ver cuál es la tendencia que siguen los precios en función del atributo.
  
Lo primero es importar `LinearRegression` y crear un objeto.

    :::python
    from sklearn.linear_model import LinearRegression
    lr = LinearRegression(normalize=True)

Una vez tenemos claro el modelo a emplear, el siguiente paso es entrenarlo con los datos de variables independientes y variables dependientes que tenemos. Para ello, en scikit-learn tenemos funciones del tipo `modelo.fit(X, y)`.

    :::python
    lr.fit(boston.data, boston.target)

Éste, al tratarse de un modelo sencillo y con muy pocas muestra tardará muy poco en entrenarse. Una vez completado el proceso podemos ver los coeficientes que ha asignado a cada atributo y así ver de qué manera contribuyen al precio final de la vivienda.

    :::python
    for (feature, coef) in zip(boston.feature_names, lr.coef_):
        print('{:&gt;7}: {: 9.5f}'.format(feature, coef))

    CRIM:  -0.10717
         ZN:   0.04640
      INDUS:   0.02086
       CHAS:   2.68856
        NOX: -17.79576
         RM:   3.80475
        AGE:   0.00075
        DIS:  -1.47576
        RAD:   0.30566
        TAX:  -0.01233
    PTRATIO:  -0.95346
          B:   0.00939
      LSTAT:  -0.52547

Con esto ya tendríamos una pequeña idea de cuales son los factores que más contribuyen a incrementar o disminuir el precio de la vivienda. Pero no vayamos a sacar conclusiones precipitadas como han hecho en su día <a href="http://www.bbc.com/news/magazine-22223190" target="_blank">Reinhart y Rogoff</a> y visualicemos los datos primero.

    :::python
    %matplotlib inline
    import matplotlib.pyplot as plt
    import numpy as np
    def plot_feature(feature):
        f = (boston.feature_names == feature)
        plt.scatter(boston.data[:,f], boston.target, c='b', alpha=0.3)
        plt.plot(boston.data[:,f], boston.data[:,f]*lr.coef_[f] + lr.intercept_, 'k')
        plt.legend(['Predicted value', 'Actual value'])
        plt.xlabel(feature)
        plt.ylabel("Median value in $1000's")
    plot_feature('AGE')


  
![age](https://pybonacci.org/images/2015/04/age.png)

En este caso hemos representado el precio medio la vivienda frente a la proporción de viviendas anteriores a 1940 que hay en la zona. Y como poder ver cláramente, emplear sólo un parámetro (AGE) para determinar el precio de la vivienda mediante una línea recta no parece lo ideal. Pero si tomamos en cuenta todas las variables las predicciones posiblemente mejoren.

Por tanto vamos a utilizar el modelo ya entrenado para predecir los precios de las viviendas. Aunque en este caso no vamos a utilizar datos nuevos, sino los mismos datos que hemos empleado para entrenar el modelo y así ver las diferencias.

    :::python
    predictions = lr.predict(boston.data)
    f, ax = plt.subplots(1)
    ax.hist(boston.target - predictions, bins=50, alpha=0.7)
    ax.set_title('Histograma de residuales')
    ax.text(0.95, 0.90, 'Media de residuales: {:.3e}'.format(np.mean(boston.target - predictions)),
            transform=ax.transAxes, verticalalignment='top', horizontalalignment='right')

![hist](https://pybonacci.org/images/2015/04/hist.png)

Podemos ver que el error medio es despreciable y que la mayoría de los valores se concentran entorno al 0. Pero, ¿cómo hemos llegado a esos valores?

La idea detrás de la regresión lineal es encontrar unos coeficientes $\beta$ que satisfagan

$$y = X\beta,$$

donde $X$ es nuestra matriz de datos e $y$ son nuestros valores objetivo. Puesto que es muy poco probable que a partir de nuestros valores de $X$ obtengamos los coeficientes que plenamente satisfagan la ecuación, es necesario añadir un término de error $\varepsilon$, tal que

$$y = X\beta + \varepsilon.$$

Con el fin de obtener ese conjunto de coeficientes $\beta$ que relacionan $X$ con $y$, `LinearRegression` recurre al método de mínimos cuadrados

$$\underset{\beta}{min\,} {|| X \beta - y||_2}^2.$$

Para éste problema también existe una solución analítica,

$$\beta = (X^T X)^{-1}X^Ty,$$

pero, ¿qué ocurre si nuestros datos no son independientes? En ese caso, $X^T X$ no es invertible y si contamos con columnas que son función de otras, o están de alguna manera correlacionadas, la estimación por mínimos cuadrados se vuelve altamente sensible a errores aleatorios incrementándose la varianza.

#### Regularización

Para esos casos emplearemos el modelo `Ridge` que añade un factor de regularización $\alpha$ que en español se conoce como <a href="http://es.wikipedia.org/wiki/Regularización_de_Tíjonov" target="_blank">factor de Tíjinov</a>.

$$\underset{\beta}{min\,} {{|| X \beta - y||\_2}^2 + \alpha {||\beta||\_2}^2},$$

y así la solución analítica queda como

$$\beta = (X^T X + \alpha^2I)^{-1}X^Ty.$$

Veamos un ejemplo. Para ello, en vez de cargar un dataset crearemos nosotros uno con tres atributos, y donde sólo dos sean linealmente independientes. Para ello utilizamos la función <a href="http://scikit-learn.org/stable/modules/generated/sklearn.datasets.make_regression.html" target="_blank"><code>make_regression</code></a>.

    :::python
    from sklearn.datasets import make_regression
    reg_data, reg_target = make_regression(n_samples=2000, n_features=3, effective_rank=2, noise=10)

Nos interesará también optimizar el valor de $\alpha$. Eso lo haremos con la validación cruzada mediante el objeto <a href="http://scikit-learn.org/stable/modules/generated/sklearn.linear_model.RidgeCV.html" target="_blank"><code>RidgeCV</code></a> que emplea una técnica similar al _leave-one-out cross-validation_ (LOOCV), i.e., dejando uno fuera para test mientras entrena con el resto de las muestras.

    :::python
    from sklearn.linear_model import RidgeCV

A la hora de crear el objeto le vamos a indicar los valores de $\alpha$ a evaluar. También guardamos los datos que obtenemos al realizar la validación cruzada con `store_cv_values=True` para representarlos gráficamente.

    :::python
    # creamos un numpy array con los valores de alpha que queremos evaluar
    alphas = np.linspace(0.01, 0.5)
    # que pasamos a nuestro modelo RidgeCV, guardando los resultados
    rcv = RidgeCV(alphas=alphas, store_cv_values=True)
    rcv.fit(reg_data, reg_target)
    # representamos gráficamente el error en función de alpha
    plt.rc('text', usetex=False)
    f, ax = plt.subplots()
    ax.plot(alphas, rcv.cv_values_.mean(axis=0))
    ax.text(0.05, 0.90, 'alpha que minimiza el error: {:.3f}'.format(rcv.alpha_),
            transform=ax.transAxes)

![ridgecv](https://pybonacci.org/images/2015/04/ridgecv.png)

Con `rcv.alpha_` obtenemos el valor de $\alpha$ que nuestro método `RidgeCV` ha considerado minimiza el error, lo cual también acabamos de comprobar gráficamente.

Pero métodos para regresión lineal hay muchos, y en la <a href="http://scikit-learn.org/stable/modules/linear_model.html#" target="_blank">documentación de scikit-learn</a> podréis encontrar una descripción bastante completa de cada alternativa.

### <a href="http://nbviewer.ipython.org/github/pybonacci/notebooks/blob/master/Machine%20Learning/Regresión%20lineal.ipynb#Regresión-no-lineal" target="_blank">Regresión no lineal</a>

Ahora bien, ¿qué hacer cuando la relación no es lineal y creemos que un polinomio haría un mejor ajuste? Si tomamos como ejemplo una función $f$ que toma la forma

$$f(x) = a + bx + cx^2 $$

la función $f$ es no lineal en función de $x$ pero si es lineal en función de los parámetros desconocidos $a$, $b$, y $c$. O visto de otra manera: podemos sustituir nuestras variables $x$ por un array $z$ tal que

$$ z = [1, x, x^2] $$

con el que podríamos reescribir nuestra función $f$ como

$$ f(z) = az\_0 + bz\_1 + cz_2$$

Para ello en `scikit-learn` contamos con la herramienta <a href="http://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.PolynomialFeatures.html" target="_blank"><code>PolynomialFeatures</code></a>. Veamos un ejemplo.

En este caso vamos a tomar la función _seno_ entre 0 y 2$\pi$ a la que añadiremos un poco de ruido.

    :::python
    f, ax = plt.subplots()
    x = np.linspace(0, 2*np.pi)
    y = np.sin(x)
    ax.plot(x, np.sin(x), 'r', label='sin ruido')
    # añadimos algo de ruido
    xr = x + np.random.normal(scale=0.1, size=x.shape)
    yr = y + np.random.normal(scale=0.2, size=y.shape)
    ax.scatter(xr, yr, label='con ruido')
    ax.legend()

![seno](https://pybonacci.org/images/2015/04/seno.png)

    :::python
    from sklearn.linear_model import Ridge
    from sklearn.preprocessing import PolynomialFeatures
    from sklearn.pipeline import make_pipeline

Scikit-learn tiene un objeto <a href="http://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.PolynomialFeatures.html" target="_blank"><code>PolynomialFeatures</code></a> que nos va a servir para convertir nuestra variable $x$ en un array $z$ del tipo $z = [1, x, x^2, \ldots, n^n]$, que es lo que nos interesa.

El resultado de esa transformación se la pasamos a nuestro modelo `Ridge`. Para facilitar la tarea en este tipo de casos —donde se realizan varios pasos que van desde el pre-tratamiento de los datos hasta un posible post-tratamiento pasando por el entrenamiento—, podemos hacer uso de las <a href="http://scikit-learn.org/stable/modules/pipeline.html" target="_blank"><code>Pipeline</code></a> que nos permiten encadenar multiples estimadores en uno. Esto es especialmente útil cuando hay secuencia de pasos predefinidos en el procesado de datos con, por ejemplo, selección de atributos, normalización y clasificación.

    :::python
    f, ax = plt.subplots()
    ax.plot(x, np.sin(x), 'r', label='sin ruido')
    ax.scatter(xr, yr, label='con ruido')
    # convertimos nuestro array en un vector columna
    X = xr[:, np.newaxis]
    # utilizamos un bucle para probar polinomios de diferente grado
    for degree in [3, 4, 5]:
        # utilizamos Pipeline para crear una secuencia de pasos
        model = make_pipeline(PolynomialFeatures(degree), Ridge())
        model.fit(X, y)
        y = model.predict(x[:, np.newaxis])
        ax.plot(x, y, '--', lw=2, label="degree %d" % degree)
    ax.legend()

![senoridge](https://pybonacci.org/images/2015/04/senoridge.png)

Acabamos de utilizar un modelo `Ridge` que implementa regularización, pero sin optimizar. ¿Qué pasaría si optimizamos el parámetro de regularización $alpha \alpha$ con `RidgeCV`?

    :::python
    f, ax = plt.subplots()
    ax.plot(x, np.sin(x), 'r', label='sin ruido')
    ax.scatter(xr, yr, label='con ruido')
    # convertimos nuestro array en un vector columna
    X = xr[:, np.newaxis]
    # utilizamos un bucle para probar polinomios de diferente grado
    for degree in [3, 4, 5]:
        # utilizamos Pipeline para crear una secuencia de pasos
        model = make_pipeline(PolynomialFeatures(degree), RidgeCV(alphas=alphas))
        model.fit(X, y)
        y = model.predict(x[:, np.newaxis])
        ax.plot(x, y, '--', lw=2, label="degree %d" % degree)
    ax.legend()

Si comparamos esta última gráfica con la anterior vemos que ahora las predicciones se han igualado entre si ofreciendo los polinomios de diferente grado predicciones prácticamente idénticas. Eso es porque la regularización tiende a penalizar la complejidad de los modelos tratando de evitar el sobreajuste (_overfitting_).

### <a href="http://nbviewer.ipython.org/github/pybonacci/notebooks/blob/master/Machine%20Learning/Regresión%20logística.ipynb" target="_blank">Regresión logística</a>

Podemos clasificar de dos formas, mediante discriminación o asignando probabilidades. Discriminando, asignamos a cada $x$ una de las $K$ clases $C\_k$. Por contra, desde un punto de vista probabilístico, lo que haríamos es asignar a cada $x$ la probabilidad de pertenecer a la clase $C\_k$. El tipo de clasificación que realicemos es a discreción del usuario y muchas veces dependerá de la distribución de los datos o de los requisitos que nos imponga el cliente. Por ejemplo, hay campeonatos en Kaggle donde lo que se pide es identificar la clase —<a href="http://www.kaggle.com/c/digit-recognizer/data" target="_blank">Digit Recognizer</a>—, pero también puede ser un requisito el determinar la probabilidad de pertecer a una clase determinada —<a href="http://www.kaggle.com/c/otto-group-product-classification-challenge/details/evaluation" target="_blank">Otto Group Product Classification Challenge</a>.

En scikit-learn podemos obtener clasificaciones de ambas maneras una vez entrenado el modelo.

  * `modelo.predict()`, para asignar una categoría.
  * `modelo.predict_proba()`, para determinar la probabilidad de pertenencia.

Aquí nos centraremos en la parte probabilística, que espero nos dé una visión más ampliar, y a su vez nos servirá para asignar una categoría si definimos un [hiperplano](https://es.wikipedia.org/wiki/Hiperplano).

Para modelos probabilísticos lo más conveniente, en el caso de contar con dos categorías, es la representación binaria donde contamos con una única variable objetivo $t \in &#123;0,1&#125;$ tal que $t=0$ representa la clase $C\_1$ y $t=1$ representa la clase $C\_2$. Podemos considerar que el valor de $t$ representa la probabilidad de que la clase sea $C_2$, con los valores de probabilidad tomando valores entre $0$ y $1$.

Veamos un ejemplo.

    :::python
    from sklearn.linear_model import LogisticRegression
    from sklearn.datasets import make_classification
    import matplotlib.pyplot as plt
    import numpy as np

Con la función `make_classification` de scikit-learn, creamos un conjunto de datos para clasificar. Para empezar vamos a contar con sólo un atributo o </em>feature</em> y dos clases o categorías. Los categorías van a estar separadas, pero permitiremos un cierto grado de solapamiento a través del parámetro `class_sep`; así, la clasificación probabilística cobra más sentido.

    :::python
    # con el parámetro random_state nos aseguramos obtener siempre lo mismo
    X, y = make_classification(n_features=1, n_informative=1, n_redundant=0, n_clusters_per_class=1,
                               class_sep=0.9, random_state=27)
    plt.scatter(X, y, alpha=0.4)
    plt.xlabel('X')
    plt.ylabel('Probabilidad')

![class](https://pybonacci.org/images/2015/04/class.png)

En regresión logística los que vamos a hacer es calcular las probabilidades $p(C_k|x)$. La función logística o [sigmoide](http://es.wikipedia.org/wiki/Función_sigmoide) nos va a permitir definir esas probabilidades y viene definida como

$$f(x) = \frac{1}{1 + \exp(-k(x-x_0))} $$

Como veremos a continuación, la sigmoide tiene forma de _S_ y la función logística juega un papel muy importante en muchos algoritmos de clasificación. Pero no es la única función de ese tipo; también podemos encontrarnos las función arcotangente, tangente hiperbólica o [softmax](https://en.wikipedia.org/wiki/Softmax_function) entre otras.

Como es costumbre en scikit-learn, primero definimos el modelo que vamos a emplear que será `LogisticRegression`. Lo cargamos con los parámetros por defecto y lo entrenamos.

    :::python
    lr = LogisticRegression()
    lr.fit(X, y)

Por defecto, en Jupyter, nos va a imprimir los parámetros con los que se ha entrenado el modelo. Una vez entrenado podemos predecir las probabilidades de pertenencia a cada categoría. Para ello, como ya hemos dicho, utilizaremos la función `predict_proba()` que toma como datos de entrada los atributos $X$.

Lo que nos devuelve la función `predict_proba()` es un array de dimensiones (n atributos, n clases). A nosotros sólo nos va a interesar representar la segunda columna, es decir, $p(C\_1|x)$, pues sabemos que $p(C\_1|x) = 1 - p(C_0|x)$.

    :::python
    plt.scatter(X, y, alpha=0.4, label='real')
    plt.plot(np.sort(X, axis=0), lr.predict_proba(np.sort(X, axis=0))[:,1], color='r', label='sigmoide')
    plt.legend(loc=2)
    plt.xlabel('X')
    plt.ylabel('Probabilidad')

![sigmoide](https://pybonacci.org/images/2015/04/sigmoide.png)

Se aprecia claramente la curva en forma de _S_ de la función logística que es lo que estábamos buscando. Esto nos dice que un punto con $x=0$ tiene aproximadamente un 50 % de probabilidades de pertenecer a cualquiera de las dos categorías.

Si a partir de las probabilidades quisiesemos hacer una clasificación por categorías no tendríamos más que definir un valor umbral. Es decir, cuando la función logística asigna una probabilidad mayor a, por ejemplo, 0.5 entonces asignamos esa categoría. Eso es básicamente lo que hace `predict()` tal y como podemos ver a continuación.

    :::python
    plt.scatter(X, y, alpha=0.4, label='real')
    plt.plot(np.sort(X, axis=0), lr.predict(np.sort(X, axis=0)), color='r', label='categoría')
    plt.legend(loc=2)
    plt.xlabel('X')
    plt.ylabel('Probabilidad')

![sigmoideumbral](https://pybonacci.org/images/2015/04/sigmoideumbral.png)

## Conclusión

Los métodos que hemos visto en ésta segunda parte son de los más sencillos que hay, pero son la base fundamental sobre la que se asientan otros métodos mucho más complejos. Por ejemplo, dentro de una red neuronal, cada neurona representa una función logística, y el conjunto de ellas es capaz de reconocer objetos en imágenes. Sencillamente impresionante.

En la tercera entrega de ésta serie seguiremos viendo métodos de aprendizaje supervisado pero con un enfoque ya más práctico. También veremos cómo competir en Kaggle a través de sus tutoriales; y una vez hayamos adquirido algo de confianza, pasar a las competiciones. La dinámica es la misma, lo que cambia es el premio.

![mnist](https://pybonacci.org/images/2015/04/mnist.png)

Espero que os haya gustado. Cualquier comentario o sugerencia es bienvenido.

## Referencias

Bishop, C. (2006). _Pattern recognition and machine learning_. New York: Springer.

Hauck, T. (2014). _Scikit-learn Cookbook_. Birmingham, U.K.: Packt Publishing.

Pedregosa, F., Varoquaux, G., Gramfort, A. et al. (2011). Scikit-learn: Machine Learning in Python. _Journal of Machine Learning Research_, 12, pp. 2825-2830.

Richert, W. and Coelho, L. (2013). _Building Machine Learning Systems with Python_. Birmingham: Packt Publishing.
