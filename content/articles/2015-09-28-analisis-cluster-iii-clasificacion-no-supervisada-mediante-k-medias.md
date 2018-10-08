---
title: Análisis Cluster (III): Clasificación no supervisada mediante K-medias
date: 2015-09-28T19:20:35+00:00
author: Kiko Correoso
slug: analisis-cluster-iii-clasificacion-no-supervisada-mediante-k-medias
tags: agrupamiento clusters, ai, aprendizaje automático, aprendizaje no supervisado, clasificación clustering, ia, inteligencia artificial, machine learning, scipy, scipy.cluster, scipy.spatial, unsupervised learning
Status: published

*(Este es el tercer capítulo de la mini-serie de artículos sobre análisis cluster que estamos haciendo en pybonacci, si todavía no has leído [los anteriores artículos les puedes echar un ojo ahora](http://pybonacci.org/tag/agrupamiento-clusters/). Escribir esta tercera parte solo ha tardado ¡¡¡tres años en salir!!!).*

El algoritmo de k-medias es uno de los algoritmos más sencillos de agrupamiento dentro del campo del aprendizaje automático (*machine learning* para los *hipsters*). Sirve para agrupar $N$-elementos en $K$-grupos distintos.

# Agrupamiento

*(Breve resumen de lo visto en anteriores artículos).*

Las técnicas de [agrupamiento o análisis _Cluster_](https://en.wikipedia.org/wiki/Cluster_analysis) son un tipo de aprendizaje no supervisado ya que no requieren un aprendizaje previo a partir de los datos.  
Son métodos para agrupar datos sin etiqueta en subgrupos. Estos subgrupos pretenden reflejar algún tipo de estructura interna.

# K-medias

El algoritmo de [K-medias](https://en.wikipedia.org/wiki/K-means_clustering) es un algoritmo de agrupamiento particional que nos crea $K$ particiones de los $N$ datos (con $N \\geqslant K$). El algoritmo se puede resumir en los siguientes pasos:

*   Seleccionar $K$ puntos de forma aleatoria en un dominio que comprende todos los puntos del conjunto de datos. estos $K$ puntos representan los centros iniciales de los grupos (lo veremos en el método `_init_centroids` de la clase `KMeans` que luego explicaremos más en detalle). No vamos a implementar ningún método de posicionamiento inicial complejo, los centros iniciales serán valores aleatorios colocados entre los umbrales mínimos y máximos del conjunto de puntos (entre las $x$, $y$ mínimas y máximas). El problema que resolveremos será en dos dimensiones, como ya podéis intuir.
*  Asignar cada punto del conjunto de datos al grupo con el centro más próximo (lo veremos en el método `_assign_centroids` de la clase `KMeans`, llegaremos en breve).
*  Recalculamos los centros de los grupos a partir de todos los datos asignados a cada grupo, es decir, calculamos el [centroide](https://es.wikipedia.org/wiki/Centroide) de cada grupo método `_recalculate_centroids` de la clase (`KMeans`).
* Repetir los dos pasos anteriores hasta que se cumpla un condición que puede ser:
  *  Se ha alcanzado un número máximo de iteraciones (no deseable).
  *  Los centroides ya no cambian más allá de un rango.
    
Nosotros solo comprobaremos el segundo ya que solo vamos a manejar conjuntos pequeños de datos. Le pondremos un límite de variación a nuestra clase `KMeans` que deberán cumplir todos los centroides. La comprobación sobre si parar las iteraciones se realizarán en el método `_check_stop` de la clase KMeans.

# Todo esto pretende ser más educativo que riguroso

La implementación que vamos a hacer será en Python puro ya que pretende ser educativa de cara a ayudar a conocer el funcionamiento del algoritmo paso a paso. Tenéis implementaciones mucho más desarrolladas, precisas, con mejor rendimiento,..., en paquetes como [scipy](http://docs.scipy.org/doc/scipy/reference/cluster.vq.html), [scikit-learn](http://scikit-learn.org/stable/modules/clustering.html#k-means) u [otros](https://pypi.python.org/pypi?%3Aaction=search&term=kmeans&submit=search).

# La implementación

**AVISO PARA NAVEGANTES**: Todo el código está pensado para funcionar en Python 3. Si usas Python 2 deberías empezar a pensar en actualizarte.

Primero escribo la clase a capón y luego la voy desgranando poco a poco. La he escrito como un iterador de forma que nos permita iterar fácilmente paso a paso (la iteración paso a paso la veremos de forma visual para intentar aportar aun mayor claridad). Para ver más sobre iteradores podéis DuckDuckGoear o ver este [enlace](http://www.diveintopython3.net/iterators.html).
            
    :::python
    class KMeans:
        def __init__(self, x, y, n_clusters = 1, limit = 10):
            self.x = x
            self.x_min = min(x)
            self.x_max = max(x)
            self.y = y
            self.y_min = min(y)
            self.y_max = max(y)
            self.n_clusters = n_clusters
            self.limit = limit
            self._init_centroids()        
            self.iterations = 0
    
        def _init_centroids(self):
            self.x_centroids = []
            self.y_centroids = []
            self.colors = []
            for i in range(self.n_clusters):
                self.x_centroids.append(randint(self.x_min, self.x_max))
                self.y_centroids.append(randint(self.y_min, self.y_max))
                r = randint(0,255)
                g = randint(0,255)
                b = randint(0,255)
                color = 'rgb({0},{1},{2})'.format(r, g, b)
                self.colors.append(color)
            self._assign_centroids()
    
        def _assign_centroids(self):
            self.c = []
            # Maximum possible distance to a centroid
            dmax  = sqrt((self.x_min - self.x_max)**2 + 
                         (self.y_min - self.y_max)**2)
            for xi, yi in zip(self.x, self.y):
                cluster = 0
                d0 = dmax
                for i in range(self.n_clusters):
                    d = sqrt((xi - self.x_centroids[i])**2 + 
                             (yi - self.y_centroids[i])**2)
                    if d &lt; d0:
                        cluster = i
                        d0 = d
                self.c.append(cluster)
    
        def _recalculate_centroids(self):
            self._x_centroids = self.x_centroids[:]
            self._y_centroids = self.y_centroids[:]
            for n in range(self.n_clusters):
                x0 = 0
                y0 = 0
                cont = 0
                for i, c in enumerate(self.c):
                    if c == n:
                        cont += 1
                        x0 += self.x[i]
                        y0 += self.y[i]
                self.x_centroids[n] = x0 / cont
                self.y_centroids[n] = y0 / cont
            self._assign_centroids()
    
        def _check_stop(self):
            for i in range(self.n_clusters):
                d = sqrt(
                    (self._x_centroids[i] - self.x_centroids[i])**2 +
                    (self._y_centroids[i] - self.y_centroids[i])**2
                    )
                if d &gt; self.limit:
                    return False
            return True
    
        def __iter__(self):
            return self
    
        def __next__(self):
            self.iterations += 1
            self._recalculate_centroids()
            stop = self._check_stop()
            if stop == True:
                raise StopIteration
            return self
    
La clase anterior paso a paso:

# Metodo `__init__`
 
    :::python
    def __init__(self, x, y, n_clusters = 1, limit = 10):
            self.x = x
            self.x_min = min(x)
            self.x_max = max(x)
            self.y = y
            self.y_min = min(y)
            self.y_max = max(y)
            self.n_clusters = n_clusters
            self.limit = limit
            self._init_centroids()        
            self.iterations = 0
    
Inicializamos la clase con los valores `xg de los puntos, los valores `y</code> de los puntos, el número de grupos a usar, `n_clusters</code> y el límite del desplazamiento de los grupos a partir del cual consideraremos que podemos parar de iterar, `limit</code>.<br /> Además, a partir del los valores introducidos, extraemos las ventana umbral donde se colocan los puntos (atributos `x_min</code>, `x_max</code>, `y_min</code> e `y_max</code>) que después usaremos para inicializar los centroides (mediante `_init_centroids</code>).
            
# Metodo `_init_centroids`

    :::python
    def _init_centroids(self):
        self.x_centroids = []
        self.y_centroids = []
        self.colors = []
        for i in range(self.n_clusters):
            self.x_centroids.append(randint(self.x_min, self.x_max))
            self.y_centroids.append(randint(self.y_min, self.y_max))
            r = randint(0,255)
            g = randint(0,255)
            b = randint(0,255)
            color = 'rgb({0},{1},{2})'.format(r, g, b)
            self.colors.append(color)
        self._assign_centroids()
    
Mediante este método, que se usa al inicializar la clase, creamos los centroides iniciales a partir de valores aleatorios situados entre los valores de `x_min`, `x_max`, `y_min` e `y_max`. Además, asignamos unos colores aleatorios a cada centroide (que luego usaremos en la visualización). Pensándolo fríamente, ahora que estoy escribiendo esto, la verdad que `colors` podría estar fuera de esta clase pero lo vamos a dejar así.

Una vez que se han creado los centroides hacemos la asignación de cada punto del conjunto de puntos $x$ e $y$ a cada centroide mediante el método `_assign_centroids`.
            
# Metodo `assign_centroids`
            
    :::python
    def _assign_centroids(self):
        self.c = []
        # Maximum possible distance to a centroid
        dmax  = sqrt((self.x_min - self.x_max)**2 + 
                     (self.y_min - self.y_max)**2)
        for xi, yi in zip(self.x, self.y):
            cluster = 0
            d0 = dmax
            for i in range(self.n_clusters):
                d = sqrt((xi - self.x_centroids[i])**2 + 
                         (yi - self.y_centroids[i])**2)
                if d &lt; d0:
                    cluster = i
                    d0 = d
            self.c.append(cluster)
    
en el atributo `c` (que es una lista) almacenamos el valor del grupo al que pertenece cada punto del conjunto de datos $x$ e $y$. Para ello, primero tenemos que calcular la distancia de cada punto a cada centroide y el que centroide que tenga menos distancia al punto será el asignado. Por tanto, en este paso, hemos de calcular $N \cdot K$ distancias.
            
# Metodo `_recalculate_centroids`
            
    :::python
    def _recalculate_centroids(self):
        self._x_centroids = self.x_centroids[:]
        self._y_centroids = self.y_centroids[:]
        for n in range(self.n_clusters):
            x0 = 0
            y0 = 0
            cont = 0
            for i, c in enumerate(self.c):
                if c == n:
                    cont += 1
                    x0 += self.x[i]
                    y0 += self.y[i]
            self.x_centroids[n] = x0 / cont
            self.y_centroids[n] = y0 / cont
        self._assign_centroids()
    
En este paso, recalculamos los centroides. Cada nuevo centroide será el centroide de los puntos asignados a ese centroide. Los antiguos centroides los conservamos para poder compararlos con los nuevos y ver si han variado poco o mucho las nuevas posiciones de los centroides. Una vez que hemos calculado los nuevos centroides y que mantenemos los antiguos asignamos los puntos a los nuevos centroides mediante el método `_assign_centroids` explicado anteriormente.
            
# Metodo `_check_stop`
            
    :::python
    def _check_stop(self):
        for i in range(self.n_clusters):
            d = sqrt(
                (self._x_centroids[i] - self.x_centroids[i])**2 +
                (self._y_centroids[i] - self.y_centroids[i])**2
                )
            if d &gt; self.limit:
                return False
        return True
    
En este método calculamos si la diferencia entre la posición de los centroides antiguos y de los nuevos es superior o inferior al límite o umbral que hemos definido al instanciar la clase. Si cualquiera de los centroides se ha movido más del umbral definido seguiremos iterando (`_check_stop` devolverá `False`), si ninguno supera el umbral le diremos que pare de iterar (`_check_stop` devolverá `True`).
            
# Metodo `__iter__` y `__next__`

    :::python
    def __iter__(self):
        return self

    def __next__(self):
        self.iterations += 1
        self._recalculate_centroids()
        stop = self._check_stop()
        if stop == True:
            raise StopIteration
        return self
    
Si os habéis leído el enlace sobre iteradores que he dejado más arriba espero que esto sea sencillo de entender.

*   El método `__iter__` no necesita mayor explicación.
*   El método `__next__` incrementa el atributo `iterations`, que no vamos a usar pero que podríamos usar para limitar, por ejemplo, el número de iteraciones, os lo dejo como ejercicio :-D, cada vez que damos un nuevo paso recalculamos los centroides y chequeamos si hay que parar la iteración porque hemos cumplido las condiciones fijadas (sí, el `stop == True` es redundante pero he pretendido que sea lo más claro posible).

# Visualización

El hecho de crear la clase como un iterador es porque he pensado que podríamos iterar en cada paso y hacer una visualización interactiva. Como la visualizazión quiero que funciones cuando el notebook está estático he recurrido a usar [Brythonmagic](https://github.com/kikocorreoso/brythonmagic).  
Si queréis saber más sobre Brythonmagic podéis leer el README del enlace anterior o ver [esta entrada](http://pybonacci.org/2014/03/03/presentando-brythonmagic/) con vídeo y todo que muestra el funcionamiento.  
Como resumen, básicamente es una _magic function_ para el notebook que nos permite usar brython (una implementación de Python 3 hecha en javascript que funciona en el navegador sin necesidad de ningún kernel detrás).  
Si no lo tienes instalado lo puedes instalar mediante `pip`.
    
           
    :::
    Downloading/unpacking brythonmagic
    Downloading brythonmagic-0.1.1.tar.gz
    Running setup.py (path:/home/kiko/pyprojs/venv-scipy/build/brythonmagic/setup.py) egg_info for package brythonmagic
    
    Requirement already satisfied (use --upgrade to upgrade): ipython&gt;=1.0 in /home/kiko/pyprojs/venv-scipy/lib/python3.4/site-packages (from brythonmagic)
    Installing collected packages: brythonmagic
    Running setup.py install for brythonmagic
    
    Successfully installed brythonmagic
    Cleaning up...

Para poder hacer uso de la extensión la hemos de cargar mediante:

`%load_ext brythonmagic`

El paso siguiente nos permite usar toda la maquinaria de brython en el navegador dentro del notebook y es el último paso para que todo funcione.

    :::
    %%HTML
    <script type="text/javascript" src="http://brython.info/src/brython\_dist.js"></script>

Podemos comprobar si funciona con el siguiente ejemplo. Después de ejecutar la celda debrías de ver un mensaje en pantalla (esto seré un poco enojante cuando lo veamos en estático puesto que siempre saltará esta ventana...):

    :::python
    %%brython
    from browser import alert
    alert('it works!')

A continuación metemos el código de la clase `KMeans` que ya hemos detallado más arriba y la llamaremos desde otras celdas brython a partir del nombre que le hemos dado en esta celda (`kmeans_class`, ver primera línea de la celda)

    :::python
    from math import sqrt
    from random import randint

    class KMeans:
        def __init__(self, x, y, n_clusters = 1, limit = 10):
            self.x = x
            self.x_min = min(x)
            self.x_max = max(x)
            self.y = y
            self.y_min = min(y)
            self.y_max = max(y)
            self.n_clusters = n_clusters
            self.limit = limit
            self._init_centroids()        
            self.iterations = 0
            
        def _init_centroids(self):
            self.x_centroids = []
            self.y_centroids = []
            self.colors = []
            for i in range(self.n_clusters):
                self.x_centroids.append(randint(self.x_min, self.x_max))
                self.y_centroids.append(randint(self.y_min, self.y_max))
                r = randint(0,255)
                g = randint(0,255)
                b = randint(0,255)
                color = &#39;rgb({0},{1},{2})&#39;.format(r, g, b)
                self.colors.append(color)
            self._assign_centroids()
        
        def _assign_centroids(self):
            self.c = []
            # Maximum possible distance to a centroid
            dmax  = sqrt((self.x_min - self.x_max)**2 + 
                         (self.y_min - self.y_max)**2)
            for xi, yi in zip(self.x, self.y):
                cluster = 0
                d0 = dmax
                for i in range(self.n_clusters):
                    d = sqrt((xi - self.x_centroids[i])**2 + 
                             (yi - self.y_centroids[i])**2)
                    if d &lt; d0:
                        cluster = i
                        d0 = d
                self.c.append(cluster)
        
        def _recalculate_centroids(self):
            self._x_centroids = self.x_centroids[:]
            self._y_centroids = self.y_centroids[:]
            for n in range(self.n_clusters):
                x0 = 0
                y0 = 0
                cont = 0
                for i, c in enumerate(self.c):
                    if c == n:
                        cont += 1
                        x0 += self.x[i]
                        y0 += self.y[i]
                self.x_centroids[n] = x0 / cont
                self.y_centroids[n] = y0 / cont
            self._assign_centroids()
        
        def _check_stop(self):
            for i in range(self.n_clusters):
                d = sqrt(
                    (self._x_centroids[i] - self.x_centroids[i])**2 +
                    (self._y_centroids[i] - self.y_centroids[i])**2
                    )
                if d &gt; self.limit:
                    return False
            return True
        
        def __iter__(self):
            return self
        
        def __next__(self):
            self.iterations += 1
            self._recalculate_centroids()
            stop = self._check_stop()
            if stop == True:
                raise StopIteration
            return self
                         
El código que figura a continuación es parte de [una librería que empecé hace un tiempo para hacer gráficos en el canvas del navegador de forma simple a partir de Brython](https://bitbucket.org/kikocorreoso/brython-bryplot/src). La funcionalidad básica está en el módulo [_base.py_](https://bitbucket.org/kikocorreoso/brython-bryplot/src/528fa4116d1f8fd1f2ab44feb537d63778edb5d5/bryplot/base.py?at=default&fileviewer=file-view-default) y lo que figura a continuación es parte de ese módulo modificado en algún sitio.  
NO VOY A EXPLICAR ESTE CÓDIGO EN DETALLE PUESTO QUE NO ES PARTE DEL PROPÓSITO DE LA ENTRADA Y NO QUIERO DESVIAR LA ATENCIÓN. SI TENÉIS ALGUNA DUDA O INTERÉS PODÉIS USAR LOS COMENTARIOS DEL BLOG PARA ELLO.  
El código a continuación permite dibujar sobre un [canvas HTML5](http://www.html5canvastutorials.com/) diferentes formas. Solo vamos a definir formas para dibujar círculos, para los puntos y los centroides de los grupos, y líneas, para mostrar qué puntos se asignan a qué centroide en cada paso.


    :::
    %%brython -s canvas_utils
    from browser import document as doc
    import math

    # Base classes for higher level objects
    class Figure:
        """
        Base class to create other elements.
        """
        def __init__(self, canvasid, 
                           facecolor = "white", 
                           edgecolor = "black", 
                           borderwidth = None):
            """        
            Parameters
            ----------
            *canvasid*: String
                String indicating the canvas id where the image should be 
                rendered.
            *facecolor*: String
                String value containing a valid HTML color
            *edgecolor*: String
                String value containing a valid HTML color
            *borderwidth*: Integer
                Value indicating the width of the border in pixels.
                If not provided it will 0 and the edgecolor will not be
                visible
            """

            if isinstance(canvasid, str):
                self.id = canvasid
            else:
                raise Exception("The canvasid parameter should be a string")
                 
            try:
                self.canvas = doc[self.id]
            except:
                raise Exception("No HTML element with id=%s" %
                                self.id)
            
            try:
                self._W = self.canvas.width
                self._H = self.canvas.height
                self._ctx = self.canvas.getContext("2d")
            except:
                raise Exception("You must provide the ID of a &lt;canvas&gt; element")
            
            self.facecolor = facecolor
            self.borderwidth = borderwidth
            self.edgecolor = edgecolor
            self.clf()
        
        def clf(self):
            "clear the figure"
            self._ctx.save()
            
            # The following line should clear the canvas but I found a
            # problem when I use beginPath ¿¿¿???
            #self._ctx.clearRect(0, 0, self._W, self._H)
            # So I use the following line that is less performant but
            # this operation shouldn&#39;t be done very often...
            self.canvas.width = self.canvas.width
            
            self._ctx.fillStyle = self.facecolor
            self._ctx.fillRect(0, 0, self._W, self._H)
            self._ctx.fill()
            if self.borderwidth:
                self._ctx.lineWidth = self.borderwidth
                self._ctx.strokeStyle = self.edgecolor
                self._ctx.strokeRect(0, 0, self._W, self._H)
                self._ctx.stroke()
            self._ctx.restore()
            

    class Shape:
        """
        Base class to create other elements.
        """
        def __init__(self, context, x, y,
                           facecolor = "black", 
                           edgecolor = "black",
                           #alpha = 1,
                           borderwidth = None):
            """        
            Parameters
            ----------
            *context*: a canvas context
                a valid canvas context where the text will be rendered
            *x*: int or float
                x value for location in pixels
            *y*: int or float
                y value for location in pixels
            *facecolor*: String
                String value containing a valid HTML color
            *edgecolor*: String
                String value containing a valid HTML color
            *alpha*: int or float
                Value between 0 (transparent) and 1 (opaque) to set the
                transparency of the text
            *borderwidth*: Integer
                Value indicating the width of the border in pixels.
                If not provided it will 0 and the edgecolor will not be
                visible
            """
            self._ctx = context
            self.x = x
            self.y = y
            self.facecolor = facecolor
            self.borderwidth = borderwidth
            self.edgecolor = edgecolor
            #self.alpha = alpha

    class Circle(Shape):
        def __init__(self, *args, radius = 10, **kwargs):
            """
            Parameters
            ----------
            *radius*: int or float
                radius of the circle in pixels.
            """
            Shape.__init__(self, *args, **kwargs)
            self.r = radius
            self.draw()
        
        def draw(self):
            self._ctx.save()
            #self._ctx.globalAlpha = self.alpha
            self._ctx.beginPath()
            self._ctx.fillStyle = self.facecolor
            self._ctx.arc(self.x, self.y, self.r, 0, 2 * math.pi)
            self._ctx.fill()
            if self.borderwidth:
                self._ctx.lineWidth = self.borderwidth
                self._ctx.strokeStyle = self.edgecolor
                self._ctx.arc(self.x, self.y, self.r, 0, 2 * math.pi)
                self._ctx.stroke()
            self._ctx.closePath()
            self._ctx.restore()

    class Line(Shape):
        def __init__(self, *args, polygon = False, borderwidth = 2, **kwargs):
            Shape.__init__(self, *args, **kwargs)
            self.borderwidth = borderwidth
            self.polygon = polygon
            self.draw()
        
        def draw(self):
            self._ctx.save()
            #self._ctx.globalAlpha = self.alpha
            self._ctx.beginPath()
            self._ctx.moveTo(self.x[0], self.y[0])
            for i in range(len(self.x)):
                self._ctx.lineTo(self.x[i], self.y[i])
            if self.polygon:
                self._ctx.closePath()
                if self.facecolor:
                    self._ctx.fillStyle = self.facecolor
                    self._ctx.fill()
            if self.borderwidth:
                self._ctx.lineWidth = self.borderwidth
                self._ctx.strokeStyle = self.edgecolor
                self._ctx.stroke()
            self._ctx.restore()

El siguiente código solo nos va a valer para establecer una mínima disposición de los elementos contenidos en la visualización.  
Se incluye un canvas, donde se dibujarán las cosas, y un botón, para poder iterar el algoritmo.

    :::html
    html = """
        <div id="main">
         <p>
         <canvas id="cnvs01" width=500 height=500></canvas>
         </p>
         <p>
         <button id="button" class="btn">Next step</button>
         </p>
        </div>
    """

Por último, este es el código que realiza todo a partir de los demás. Voy a intentar explicarlo un poco más en detalle:

    :::python
    fig = Figure('cnvs01', borderwidth = 2)
    
    n_points = 50
    x = [randint(10, fig._W - 10) for value in range(n_points)]
    y = [randint(10, fig._H - 10) for value in range(n_points)]
    
    kmeans = KMeans(x, y, n_clusters = 4, limit = 1)
    
    def plot(obj):
        fig._ctx.save()
        fig._ctx.fillStyle= "#ffffff"
        fig._ctx.globalAlpha = 0.3
        fig._ctx.fillRect(2,2,fig._W-4,fig._H-4)
        fig._ctx.restore()
        x = obj.x
        y = obj.y
        npoints = len(x)
        colors = obj.colors
        xc = obj.x_centroids
        yc = obj.y_centroids
        c = obj.c
        for i in range(npoints):
            color = colors[c[i]]
            Line(fig._ctx, [x[i], xc[c[i]]], [y[i], yc[c[i]]],
                 facecolor = color, edgecolor = color)
            Circle(fig._ctx, x[i], y[i], 
                   facecolor = color, edgecolor = 'black',
                   borderwidth = 1, radius = 4)
        for xci, yci, color in zip(xc, yc, colors):
            Circle(fig._ctx, xci, yci, 
                   facecolor = color, edgecolor = 'black',
                   borderwidth = 1, radius = 8)
    
    def update(ev):
        plot(kmeans)
        try:
            next(kmeans)
        except:
            #doc['button'].disabled = True
            del doc['button']
    
    doc['button'].bind('click', update)    
                  
* `fig = Figure('cnvs01', borderwidth = 2)` inicializamos el canvas con un borde negro usando la clase Figure creada más arriba.
* Definimos el número de puntos a usar y las posiciones de los puntos.
* Inicializamos el objeto mediante `kmeans = KMeans(x, y, n_clusters = 4, limit = 1)g. En este caso queremos que tenga 4 clusters (`n_clusters`) y que el límite (`limit`) para dejar de iterar sea cuando los centroides se muevan un pixel o menos.

La función `plotg hace varias cosas.

Primero suaviza los colores de la imagen previa antes de la actual iteración (esto está más relacionado con el canvas HTML5 y con javascript y no hace falta entenderlo mucho más allá de lo comentado en esta línea)

    :::python
    fig._ctx.save()
    fig._ctx.fillStyle= "#ffffff"
    fig._ctx.globalAlpha = 0.3
    fig._ctx.fillRect(2,2,fig._W-4,fig._H-4)
    fig._ctx.restore()

Después extraemos todos los datos del objeto (`kmeansg) que vamos a usar dentro de la función.

    :::python
    x = obj.x
    y = obj.y
    npoints = len(x)
    colors = obj.colors
    xc = obj.x_centroids
    yc = obj.y_centroids
    c = obj.c
                        
Dibujamos las líneas entre los puntos y los centroides y los puntos con colores asociados a cada grupo

    :::python
    for i in range(npoints):
       color = colors[c[i]]
       Line(fig._ctx, [x[i], xc[c[i]]], [y[i], yc[c[i]]],
            facecolor = color, edgecolor = color)
       Circle(fig._ctx, x[i], y[i], 
              facecolor = color, edgecolor = 'black',
              borderwidth = 1, radius = 4)

Y finalmente se dibujan los centroides de cada grupo con un círculo un poco más grande que los propios puntos:

    :::python
    for xci, yci, color in zip(xc, yc, colors):
       Circle(fig._ctx, xci, yci, 
              facecolor = color, edgecolor = 'black',
              borderwidth = 1, radius = 8)
                     
Creamos, además, una función `updateg que será la que llama a la función `plot</code> y la que llama a una nueva iteración. El código que figura en el bloque `except`, `del `doc['button']`, es más de la parte de brython y sirve para que el botón desaparezca una vez que el iterador ha quedado exhausto (se han agotado las iteraciones).
                      
La última línea de código, `doc['button'].bind('click', update)`, asocia el evento `click` del botón a la función `update` que he comentado anteriormente.

Si ahora ejecutamos la siguiente celda de código deberíamos ver un canvas de 500px x 500px con un botón debajo. Si vamos pulsando al botón veremos como nueva iteración en acción, además de ver las anteriores iteraciones de forma difuminada. Una vez que hemos alcanzado la condición de que los centroides no se mueven más desaparecerá el botón (para no teneros ahí pulsando y que me digáis que eso no sigue funcionando...).

    :::python
    %% brython -S kmeans_class canvas_utils -h html

    fig = Figure(&#39;cnvs01&#39;, borderwidth = 2)

    n_points = 50

    x = [randint(10, fig._W - 10) for value in range(n_points)]
    y = [randint(10, fig._H - 10) for value in range(n_points)]

    kmeans = KMeans(x, y, n_clusters = 4, limit = 1)

    def plot(obj):
        fig._ctx.save()
        fig._ctx.fillStyle= "#ffffff"
        fig._ctx.globalAlpha = 0.3
        fig._ctx.fillRect(2,2,fig._W-4,fig._H-4)
        fig._ctx.restore()
        x = obj.x
        y = obj.y
        npoints = len(x)
        colors = obj.colors
        xc = obj.x_centroids
        yc = obj.y_centroids
        c = obj.c
        for i in range(npoints):
            color = colors[c[i]]
            Line(fig._ctx, [x[i], xc[c[i]]], [y[i], yc[c[i]]],
                 facecolor = color, edgecolor = color)
            Circle(fig._ctx, x[i], y[i], 
                   facecolor = color, edgecolor = &#39;black&#39;,
                   borderwidth = 1, radius = 4)
        for xci, yci, color in zip(xc, yc, colors):
            Circle(fig._ctx, xci, yci, 
                   facecolor = color, edgecolor = &#39;black&#39;,
                   borderwidth = 1, radius = 8)

    def update(ev):
        plot(kmeans)
        try:
            next(kmeans)
        except:
            #doc[&#39;button&#39;].disabled = True
            del doc[&#39;button&#39;]
            
    doc['button'].bind('click', update)
                    
Podéis ver todo el código contenido en una página web [aquí](http://kikocorreoso.bitbucket.org/kmeans/) 
                   
# Conclusiones
 
Espero que haya quedado claro el funcionamiento básico del algoritmo K-Medias. También espero que si veis alguna errata en el código me aviséis o hagáis un **Pull Request** a nuestro repositorio de notebooks.

Podéis ver este notebook funcionando incluso en estático en [el siguiente enlace](http://nbviewer.jupyter.org/github/Pybonacci/notebooks/blob/master/K-Medias.ipynb).
