---
title: Introducción a Machine Learning con Python (Parte 1)
date: 2015-01-14T22:00:02+00:00
author: Pablo Fernández
slug: introduccion-a-machine-learning-con-python-parte-1
tags: dataset, iris, kaggle, machine learning, python, scikit-learn

Desde que escuché hablar de Kaggle por primera vez, precisamente <a href="https://twitter.com/Pybonacci/status/414742882679934977" target="_blank">a través de Pybonacci</a>, me entró curiosidad por eso del _data science_ y me propuse como un reto el participar en una de sus competiciones. Para aquel que no la conozca todavía, <a title="Kaggle" href="http://www.kaggle.com/" target="_blank">Kaggle</a> es una plataforma que aloja competiciones de análisis de datos y modelado predictivo donde compañías e investigadores aportan sus datos mientras que estadistas e ingenieros de datos de todo el mundo compiten por crear los mejores modelos de predicción o clasificación.

Muchas y muy diferentes técnicas se pueden aplicar al procesado de datos para generar predicciones, estimaciones o clasificaciones. Desde técnicas de <a href="http://es.wikipedia.org/wiki/Regresión_logística" target="_blank">regresión logística</a> hasta <a href="http://es.wikipedia.org/wiki/Red_neuronal_artificial" target="_blank">redes neuronales artificiales</a> pasando por <a href="http://es.wikipedia.org/wiki/Red_bayesiana" target="_blank">redes bayesianas</a>, <a href="http://es.wikipedia.org/wiki/Máquinas_de_vectores_de_soporte" target="_blank">máquinas de vectores de soporte</a> o <a href="http://es.wikipedia.org/wiki/Árbol_de_decisión" target="_blank">árboles de decisión</a>, en Kaggle no descartan ningún método, e incluso se fomenta la cooperación entre personas con experiencia en diferentes campos para obtener el mejor modelo posible. Varias de estas técnicas se encuadran dentro de lo que es el Machine Learning, o aprendizaje automático, que nos explica <a href="http://en.wikipedia.org/wiki/Jeremy_Howard_(entrepreneur)" target="_blank">Jeremy Howard</a> en el siguiente vídeo.



<!--more Sigue leyendo... >-->

En resumen, el objetivo del machine learning (ML) es enseñar a las máquinas el llevar a cabo ciertas tareas enseñándoles algunos ejemplos de cómo o cómo no llevar a cabo la tarea. Esto rara vez es un proceso en cascada y, en multitud de ocasiones, habrá que retroceder varios pasos para probar diferentes estrategias sobre el conjunto de datos con diferentes algoritmos ML. En palabras de Richert y Coelho (2013), es éste carácter exploratorio lo que se ajusta a la perfección a Python.

> Being an interpreted high-level programming language, it may seem that Python was designed specifically for the process of trying out different things. What is more, it does this very fast.

Visto el potencial de Python en este campo, la comunidad de desarrolladores ha aportado varios paquetes como <a href="http://pybrain.org/pages/home" target="_blank">PyBrain</a> (Schaul et al., 2010) o <a href="http://scikit-learn.org/stable/index.html" target="_blank">scikit-learn</a> (Pedregosa et al., 2011) entre otros al campo del aprendizaje automático. De todos ellos, el más conocido tal vez sea scikit-learn, y es el que utilizaremos más a menudo para ilustrar los ejemplos.

Pero antes de meternos de lleno al aprendizaje automático vamos a ver unos ejercicios de clasificación básicos que nos permitirán entender mejor la posibilidades y limitaciones de algoritmos mucho más complejos.

## El _Iris flower dataset_

El conjunto de datos de la planta Iris data de los años '30 y es empleado con frecuencia como ejemplo por diferentes librerías que trabajan con datos o gráficos como <a href="http://pandas.pydata.org/pandas-docs/stable/visualization.html#andrews-curves" target="_blank">pandas</a> o el propio <a href="http://scikit-learn.org/stable/auto_examples/datasets/plot_iris_dataset.html" target="_blank">scikit-learn</a>. De cada planta de la especie Iris (setosa, versicolor y virginica) se han tomado medidas de longitud y ancho de sépalo y pétalo. Y la pregunta que se suele plantear es: _si vemos una nueva planta en el campo, ¿podríamos predecir correctamente su especie a partir de sus medidas?_

Este es un problema de aprendizaje supervisado o clasificación. Puesto que el conjunto de datos es pequeño, hemos representado las proyecciones bidimensionales como subgráficos de un solo gráfico con el que podemos identificar dos grandes grupos: uno formado por Iris Setosa y otro formado por una mezcla de Iris Versicolor e Iris Virginica.

### Primer modelo de clasificación

Nuestro primer modelo de clasificación se basará precisamente en esa primera agrupación visual que hemos realizado. Es decir, si la longitud del pétalo es inferior a 2, entonces se trata de Iris Setosa, si no, puede ser Iris Versicolor o Iris Virginica.

    :::python
    from sklearn import datasets
    # leemos el dataset
    iris = datasets.load_iris()
    # El dataset contiene 4 atributos
    print(iris.feature_names)
    # Separamos Iris Setosa de las otras dos especies en función de la longitud
    # del pétalo (tercer atributo).
    for value in iris.data[:, 2]:
        if value > 2:
            print('Iris setosa')
        else:
            print('Iris virginica o Iris versicolor')

Lo que hemos creado es un simple umbral en una de las dimensiones. Lo hemos hecho de manera visual; el aprendizaje automático tiene lugar cuando escribimos código que realiza esto mismo por nosotros.

Distinguir Iris Setosa de las otras dos especies fue sencillo. Sin embargo, no tenemos forma de ver inmediatamente cuál es el mejor umbral para distinguir Iris Virginica de Iris Versicolor. Es más, podemos deducir que la distinción nunca será perfecta. Pero podemos generar un algoritmo sencillo que nos de la mejor solución de compromiso en base a los parámetros medidos de las plantas.

En el siguiente fragmento de código vamos a buscar, de entre las cuatro características medidas —longitud y ancho de sépalo y pétalo—, el valor de umbral que mejor clasifica la familia de Iris.

    :::python
    from sklearn import datasets
    import pandas as pd
    # leemos el dataset y pasamos los datos a una DataFrame de pandas por comodidad
    sk_iris = datasets.load_iris()
    iris = pd.DataFrame(data=sk_iris.data, columns=sk_iris.feature_names)
    iris['labels'] = pd.Categorical.from_codes(sk_iris.target, sk_iris.target_names)
    # descartamos la familia setosa que ya tenemos clasificada
    iris = iris[iris.labels != 'setosa']
    virginica = iris.labels=='virginica'
    # obtenemos un array con los nombres de las características que medimos
    features = iris.columns[:4]
    # inicializamos en valor de precisión
    best_acc = 0.0
    for fi in features:                    # Por cada parámetro o característica de la que tenemos valores
        thresh = iris[fi].copy()           # obtenemos una lista de valores para el umbral
        thresh.sort_values(inplace=True)   # que ordenamos de menor a mayor.
        for t in thresh:                   # Por cada posible valor de umbral
            pred = (iris[fi] > t)          # determinamos los elementos de la tabla que están por encima
            acc = (pred==virginica).mean() # y calculamos que porcentaje de la familia virginica está recogida.
            if acc > best_acc:             # Si mejoramos la detección, actualizamos los parámetro de la colección.
                best_acc = acc             # Mejor precisión obtenida.
                best_fi = fi               # Mejor característica para clasificar las familias.
                best_t = t                 # Valor óptimo de umbral.

    print('Mejor precisión obtenida: {:.1%}'.format(best_acc))
    print('Mejor característica para clasificar: {}'.format(best_fi))
    print('Valor óptimo de umbral: {} cm'.format(best_t))

Según el algoritmo que hemos implementado, el valor óptimo de umbral es de 1.6 cm de ancho de pétalo. Con ese valor, clasificamos correctamente el 94% de las plantas como Virginica. En este tipo de modelos de umbral, la frontera de decisión será siempre paralela a uno de los ejes.

### Validación cruzada

El modelo, a pesar de su simplicidad, logra un 94% de acierto sobre los datos de entrenamiento. No obstante, se trata de una valoración bastante optimista pues empleamos los propios datos de entrenamiento para evaluar el modelo. Lo que realmente queremos es estimar la habilidad del modelo de generalizar en nuevos casos.

Para determinar las capacidades del modelo, u obtener un modelo más robusto, se suele recurrir a la <a href="http://es.wikipedia.org/wiki/Validación_cruzada" target="_blank">validación cruzada</a>. De esta manera utilizamos parte de los datos de que disponemos para entrenar el modelo —_training set_—, y el resto de datos para probarlo —_test set_— (ver imagen inferior).<figure style="width: 526px" class="wp-caption aligncenter">

<img src="http://upload.wikimedia.org/wikipedia/commons/f/f2/K-fold_cross_validation.jpg" width="526" height="262" class /><figcaption class="wp-caption-text">Validación cruzada de k=4 iteraciones [<a href="http://es.wikipedia.org/wiki/Validaci%C3%B3n_cruzada#Error_de_la_validaci.C3.B3n_cruzada_de_K_iteraciones" target="_blank">Fuente</a>].</figcaption></figure>

### K nearest neighbors

Un paso más hacia lo que sería _machine learning_ es el método <a href="http://es.wikipedia.org/wiki/Knn" target="_blank"><em>k</em>-nn</a> de clasificación supervisada. En este caso, a la hora de clasificar un nuevo elemento, buscamos en el conjunto de datos de que disponemos al punto, o _k_-puntos más cercanos, y le asignamos su catogoría.

Si bien podemos <a href="http://machinelearningmastery.com/tutorial-to-implement-k-nearest-neighbors-in-python-from-scratch/" target="_blank">implementar el algoritmo a mano en Python</a> —nunca está de más saber cómo funcionan las cosas—, scikit-learn incluye la herramienta <a href="http://scikit-learn.org/stable/modules/generated/sklearn.neighbors.KNeighborsClassifier.html" target="_blank">KNeighborsClassifier</a> que ya realiza todo el trabajo pesado por nosotros. Aquí voy a adaptar ligeramente el <a href="http://scikit-learn.org/stable/auto_examples/neighbors/plot_classification.html#example-neighbors-plot-classification-py" target="_blank">ejemplo</a> que proporciona scikit-learn para utilizarlo con pandas y generar unos gráficos diferentes que nos permitan compararlo con el modelo anterior.

    :::python
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    from matplotlib.colors import ListedColormap
    from sklearn.neighbors import KNeighborsClassifier

Vamos a importar ahora el dataset que viene con scikit-learn.

    :::python
    # leemos el dataset y pasamos los datos a una DataFrame de pandas por comodidad
    sk_iris = datasets.load_iris()
    iris = pd.DataFrame(data=sk_iris.data, columns=sk_iris.feature_names)
    # que las etiquetas sean de tipo Categorical será importante más adelante a la hora de crear los gráficos
    iris['labels'] = pd.Categorical.from_codes(sk_iris.target, sk_iris.target_names)
    X = iris[['petal length (cm)', 'petal width (cm)']] # Tomamos el ancho y longitud del pétalo.
    y = iris['labels'].astype('category')

Tomaremos un número de vecinos relativamente grande, _k_ = 15. El valor de _k_ depende mucho de los datos de que dispongamos, pero en general, un valor alto mitiga el ruido a costa de diferenciar menos zonas. Definimos también el espesor de la malla y los _colormaps_ del gráfico.

    :::python
    n_neighbors = 15
    h = .02          # step size de la malla
    # Creamos los colormap
    cmap_light = ListedColormap(['#FFAAAA', '#AAFFAA', '#AAAAFF'])
    cmap_bold = ListedColormap(['#FF0000', '#00FF00', '#0000FF'])

Por último, nos metemos de lleno al modelo. Éste, en común a la mayoría de modelos en scikit-learn, dispone de una serie de funciones que se ejecutan paso a paso.

  * _nombre-del-modelo_.**fit()**
  * _nombre-del-modelo_.**predict()**
  * _nombre-del-modelo_.**score()**

Con la función `fit()` entrenamos el modelo para obtener los parámetros que utilizaremos sobre los datos de test con la función `predict()`. Finalmente, con `score()` podremos obtener una estimación de la capacidad de acierto de nuestro modelo sobre los datos de trabajo.

    :::python
    for weights in ['uniform', 'distance']:
        # Creamos una instancia de Neighbors Classifier y hacemos un fit a partir de los
        # datos.
        # Los pesos (weights) determinarán en qué proporción participa cada punto en la
        # asignación del espacio. De manera uniforme o proporcional a la distancia.
        clf = KNeighborsClassifier(n_neighbors, weights=weights)
        clf.fit(X, y.cat.codes)
        # Creamos una gráfica con las zonas asignadas a cada categoría según el modelo
        # k-nearest neighborgs. Para ello empleamos el meshgrid de Numpy.
        # A cada punto del grid o malla le asignamos una categoría según el modelo knn.
        # La función c_() de Numpy, concatena columnas.
        x_min, x_max = X.iloc[:, 0].min() - 1, X.iloc[:, 0].max() + 1
        y_min, y_max = X.iloc[:, 1].min() - 1, X.iloc[:, 1].max() + 1
        xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                             np.arange(y_min, y_max, h))
        Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])
        # Ponemos el resultado en un gráfico.
        Z = Z.reshape(xx.shape)
        plt.figure()
        plt.pcolormesh(xx, yy, Z, cmap=cmap_light)
        # Representamos también los datos de entrenamiento.
        plt.scatter(X.iloc[:, 0], X.iloc[:, 1], c=y.cat.codes, cmap=cmap_bold)
        plt.xlim(xx.min(), xx.max())
        plt.ylim(yy.min(), yy.max())
        plt.title("3-Class classification (k = %i, weights = '%s')"
                  % (n_neighbors, weights))
        plt.xlabel('Petal Width')
        plt.ylabel('Petal Length')
        plt.savefig('iris-knn-{}'.format(weights))

Las figuras que obtenemos son las siguientes.

<div id='gallery-1' class='gallery galleryid-2976 gallery-columns-2 gallery-size-thumbnail'>
  <figure class='gallery-item'>

  <div class='gallery-icon landscape'>
    <a href='https://pybonacci.org/wp-content/uploads/2015/01/iris-knn-distance.png'><img width="150" height="150" src="https://pybonacci.org/wp-content/uploads/2015/01/iris-knn-distance-150x150.png" class="attachment-thumbnail size-thumbnail" alt="" aria-describedby="gallery-1-3078" /></a>
  </div><figcaption class='wp-caption-text gallery-caption' id='gallery-1-3078'> 3-Class classification (k = 15, weights=&#8217;distance&#8217;) </figcaption></figure><figure class='gallery-item'>

  <div class='gallery-icon landscape'>
    <a href='https://pybonacci.org/wp-content/uploads/2015/01/iris-knn-uniform.png'><img width="150" height="150" src="https://pybonacci.org/wp-content/uploads/2015/01/iris-knn-uniform-150x150.png" class="attachment-thumbnail size-thumbnail" alt="" aria-describedby="gallery-1-3077" /></a>
  </div><figcaption class='wp-caption-text gallery-caption' id='gallery-1-3077'> 3-Class classification (k = 15, weights=&#8217;uniform&#8217;) </figcaption></figure>
</div>

Como podemos ver, en este caso, las lineas que separan las tres categorías de planta Iris ya no son verticales. El modelo _k_ Nearest Neighborgs que hemos empleado ha considerado que la separación de categorías (para selección de ordenadas y abscisas) es más bien inclinada. Visualmente también podemos apreciar que éste modelo incluye más puntos dentro de la categoría correcta que el modelo simple que hemos estudiado en primer lugar. Si recurrimos a la función `score()`, obtendremos una puntuación del 96% en el caso de `weights='uniform'`, y del 98.6% si optamos por `weights='distancia'`. Cabe recordar que en este caso tampoco se ha recurrido a un _cross validation_ para puntuar el modelo, por lo que esta puntuación puede ser algo optimista.

## Conclusión

Espero que a esta primera parte le siga al menos una segunda, donde si que espero poder enseñar algo de Machine Learning de verdad. No soy ni mucho menos un aficionado en esto del ML, pues hace bien poco que he empezado, pero como es algo por lo que siempre he sentido un cierto interés, creo que merece la pena el que me embarque en enseñar lo que voy aprendiendo; y ver si así despierto el interés de más gente por el tema, perderle el miedo y no verlo como algo lejano y muy complicado.

Por ahora no ha sido más que una introducción y prácticamente no se ha tocado nada de aprendizaje automático, pero hemos tratado algunos conceptos básicos que son clave asimilar primero para poder desarrollar adecuadamente nuestra intuición en la materia. Recalcar, además, la importancia de la estimación del error del modelo. En la próxima entrada explicaré como funciona Kaggle en ese aspecto, con datos de entrenamiento y de test, con _leaderboard_ público y privado.

Cualquier comentario o sugerencia respecto a la entrada es bien recibida. Críticas también. Palos, no. Os leo.

## Referencias

Kaggle.com, (2015). _Kaggle: The Home of Data Science_. [online] Available at: http://kaggle.com [Accessed 10 Jan. 2015].

Pedregosa, F., Varoquaux, G., Gramfort, A. et al. (2011). Scikit-learn: Machine Learning in Python. _Journal of Machine Learning Research_, 12, pp. 2825–2830.

Richert, W. and Coelho, L. (2013). _Building Machine Learning Systems with Python_. Birmingham: Packt Publishing.

Schaul, T., Bayer, J., Wierstra, D. et al. (2010). PyBrain. _Journal of Machine Learning Research_, 11, pp. 743–746.
