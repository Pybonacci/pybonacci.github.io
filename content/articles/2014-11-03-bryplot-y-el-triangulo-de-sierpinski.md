---
title: BryPlot y el triángulo de Sierpinski
date: 2014-11-03T18:23:56+00:00
author: Kiko Correoso
slug: bryplot-y-el-triangulo-de-sierpinski
tags: bryplot, brython, canvas, html5, recursión, sierpinski

Esta vez vamos a ver como usar una pequeña librería que he creado para poder dibujar en el canvas de HTML5 usando python (vía Brython).

La librería la podéis encontrar en este [repo alojado en bitbucket](https://bitbucket.org/kikocorreoso/brython-bryplot). Solo voy a usar el módulo base y para no complicar el tema lo voy a pegar como código directamente aquí y así no habrá que importarlo.

Pero primero algunos apuntes:

# ¿Para qué otra librería para dibujar?

Por varios motivos:

  * Porque encontré algo de tiempo.
  * Porque me da la gana 😛
  * Para aprender a usar canvas.
  * Para aprender sobre el DOM, eventos,...
  * Para aprender.

# Preparativos antes de empezar.

Para poder usar este engendro dentro del notebook de IPython vamos a usar una extensión creada para ello. La extensión se llama [brythonmagic](https://github.com/kikocorreoso/brythonmagic) (¡qué derroche de creatividad!) y permite usar brython internamente en el notebook de IPython.

Para instalarla solo tenéis que hacer:

<pre class="language-python"><code>%install_ext https://raw.github.com/kikocorreoso/brythonmagic/master/brythonmagic.py</code></pre>

Y para poder usarla hacemos:

<pre class="language-python"><code>%load_ext brythonmagic</code></pre>

Además, hemos de cargar la librería javascript brython.

<pre class="language-python"><code class="language-python" data-language="python">%%HTML
&lt;script src="http://brython.info/src/brython_dist.js"&gt;&lt;/script&gt;</code></pre>

# Cargamos el módulo base directamente en el notebook.

Una vez listo para empezar a usar brython en el notebook vamos a meter en la siguiente celda el módulo `base`, citado anteriormente, y que contiene una serie de clases para poder dibujar texto y formas simples (círculos, cuadrados, polilíneas,...) en el `canvas`.

<pre class="language-python"><code class="language-python" data-language="python">%%brython -s base
from browser import document as doc
import math

## Base classes for higher level objects
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
            raise Exception("You must provide the ID of a &lt;canvas> element")
        
        self.facecolor = facecolor
        self.borderwidth = borderwidth
        self.edgecolor = edgecolor
        self.clf()
    
    def clf(self):
        "clear the figure"
        self._ctx.save()
        
        # The following line should clear the canvas but I found a
        # problem when I use beginPath Â¿Â¿Â¿jQuery2030011017107678294003_1414965477473?
        #self._ctx.clearRect(0, 0, self._W, self._H)
        # So I use the following line tat is less performant but
        # this operation shouldn't be done very often...
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
        

class Text:
    """
    Base class for text
    """
    def __init__(self, context, x, y, s, 
                       font = "Verdana", fontsize = 12,
                       horizontalalignment='center',
                       verticalalignment='middle',
                       color = "black",
                       alpha = 1,
                       rotate = 0):
        """
        Parameters
        ----------
        *context: a canvas context
            a valid canvas context where the text will be rendered
        *x*: int or float
            x value for location in pixels
        *y*: int or float
            y value for location in pixels
        *s*: String
            String value with the text to be rendered
        *font*: String
            String value with the font type
        *fontsize*: int or float
            Size of the font in pixels
        *horizontalalignment*: String
            ``left``, ``right`` or ``center``
        *verticalalignment*: String
            ``top``, ``bottom``, ``middle``
        *color*: String
            A string with a valid HTML color
        *alpha*: int or float
            Value between 0 (transparent) and 1 (opaque) to set the
            transparency of the text
        *rotate*: int or float
            Value indicating an angle to rotate the text in the
            clockwise direction
        """
        self._ctx = context
        self.x = x
        self.y = y
        self.s = s
        self.font = font
        self.fontsize = fontsize
        self.font_complete = "{0}pt {1} sans-serif".format(fontsize,
                                                            font)
        self.horizontalalignment = horizontalalignment
        self.verticalalignment = verticalalignment
        self.color = color
        self.alpha = alpha
        self.rotate = rotate
        self.draw()
    
    def draw(self):
        self._ctx.save()
        self._ctx.translate(self.x, self.y)
        self._ctx.rotate(self.rotate * math.pi/ 180.)
        self._ctx.textAlign = self.horizontalalignment
        self._ctx.textBaseline = self.verticalalignment
        self._ctx.font = self.font_complete
        self._ctx.globalAlpha = self.alpha
        self._ctx.fillStyle = self.color
        self._ctx.fillText(self.s, 0, 0)
        _ = self._ctx.measureText(self.s)
        self.text_width = _.width
        self._ctx.restore()
    
    @property
    def transparency(self):
        return self.alpha
    
    @transparency.setter
    def transparency(self, alpha):
        if alpha &gt;= 0 and alpha &lt;= 1:
            self.alpha = alpha
        else:
            print("alpha value must be between 0 and 1")
    
    # create more setters and getters for other properties?
        
class Shape:
    """
    Base class to create other elements.
    """
    def __init__(self, context, x, y,
                       facecolor = "black", 
                       edgecolor = "black",
                       alpha = 1,
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
        self.alpha = alpha

class Rectangle(Shape):
    def __init__(self, *args, size = (0,0), rotation = 0, **kwargs):
        """
        Parameters
        ----------
        *size*: tuple
            (width, height) size of the rectangle in pixels.
        *rotation*: int or float
            Value indicating an angle to rotate the shape in the
            clockwise direction         
        """
        Shape.__init__(self, *args, **kwargs)
        self.x_size = size[0]
        self.y_size = size[1]
        self.rotation = rotation
        self.draw()
    
    def draw(self):
        self._ctx.save()
        self._ctx.globalAlpha = self.alpha
        x0 = -self.x_size / 2.
        y0 = -self.y_size / 2.        
        self._ctx.translate(self.x, self.y)
        self._ctx.rotate(self.rotation * math.pi / 180.)
        self._ctx.fillStyle = self.facecolor
        self._ctx.fillRect(x0, y0, self.x_size, self.y_size)
        self._ctx.fill()
        if self.borderwidth:
            self._ctx.lineWidth = self.borderwidth
            self._ctx.strokeStyle = self.edgecolor
            self._ctx.strokeRect(x0, y0, self.x_size, self.y_size)
            self._ctx.stroke()
        self._ctx.restore()

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
        self._ctx.globalAlpha = self.alpha
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

class Wedge(Shape):
    def __init__(self, *args, radius = 10, angle = 30, rotation = 0, **kwargs):
        """
        Parameters
        ----------
        *radius*: int or float
            radius of the pie wedge in pixels.
        *angle*: int or float
            angle width in degrees.
        *rotation*: int or float
            Value indicating an angle to rotate the shape in the
            clockwise direction 
        """
        Shape.__init__(self, *args, **kwargs)
        self.r = radius
        self.angle = angle
        self.rotation = rotation
        self.draw()
    
    def draw(self):
        self._ctx.save()
        self._ctx.globalAlpha = self.alpha
        self._ctx.fillStyle = self.facecolor
        self._ctx.beginPath()
        self._ctx.arc(self.x, self.y, self.r, 
                      (self.rotation - self.angle / 2 - 90) * math.pi / 180.,
                      (self.rotation + self.angle / 2 - 90) * math.pi / 180., 
                      False)
        self._ctx.lineTo(self.x, self.y)
        self._ctx.closePath()
        self._ctx.fill()
        if self.borderwidth:
            self._ctx.lineWidth = self.borderwidth
            self._ctx.strokeStyle = self.edgecolor
            self._ctx.arc(self.x, self.y, self.r, 
                      (self.rotation - self.angle / 2 - 90) * math.pi / 180.,
                      (self.rotation + self.angle / 2 - 90) * math.pi / 180., 
                      False)
            self._ctx.stroke()
        self._ctx.restore()

class Line(Shape):
    def __init__(self, *args, polygon = False, borderwidth = 2, **kwargs):
        Shape.__init__(self, *args, **kwargs)
        self.borderwidth = borderwidth
        self.polygon = polygon
        self.draw()
    
    def draw(self):
        self._ctx.save()
        self._ctx.globalAlpha = self.alpha
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

class Polygon(Line):
    def __init__(self, *args, polygon = True, 
                 facecolor = None, **kwargs):
        Line.__init__(self, *args, **kwargs)
        self.polygon = polygon
        self.facecolor = facecolor
        self.draw()&lt;/canvas></code></pre>

Básicamente, el módulo que acabamos de cargar nos permite usar el canvas de HTML5 a un nivel más alto que usando la API oficial y con una sintaxis pythónica.

Para ver todas las posibilidades actuales de la librería podéis usar [este notebook que está en el mismo repo de la librería](http://nbviewer.ipython.org/urls/bitbucket.org/kikocorreoso/brython-bryplot/raw/2de8de16b41b241a295bcd2759ff0c008597dc13/Testing_Bryplot.ipynb).

# Ejemplo de uso, el triángulo de Sierpinski.

El triángulo de Sierpinski es un fractal y es lo que vamos a dibujar para ver las ¿capacidades? de Bryplot.

Primero hemos de crear el elemento HTML donde vamos a dibujar y que posteriormente le pasaremos al script Brython para que lo use.

<pre class="language-python"><code>HTML = """&lt;div&gt;&lt;canvas id="cnvs01" width=500 height=433&gt;&lt;/canvas&gt;&lt;/div&gt;"""</code></pre>

Y ahora vamos a crear simplemente la figura, que es donde pintaremos todo lo que queramos, con un fondo negro:

<pre class="language-python"><code class="language-python" data-language="python">%%brython -S base -h HTML
fig = Figure('cnvs01', facecolor = "black")</code></pre>

[<img class="alignnone size-full wp-image-2869" src="http://pybonacci.org/wp-content/uploads/2014/11/BRYPLOT01.png" alt="BRYPLOT01" width="500" height="433" srcset="https://pybonacci.org/wp-content/uploads/2014/11/BRYPLOT01.png 500w, https://pybonacci.org/wp-content/uploads/2014/11/BRYPLOT01-300x259.png 300w" sizes="(max-width: 500px) 100vw, 500px" />](http://pybonacci.org/wp-content/uploads/2014/11/BRYPLOT01.png)

Ahora vamos a dar un pequeño paso más y vamos a dibujar un triángulo usando la clase `Polygon`. A esta clase le hemos de pasar el contexto del canvas que, dicho de forma muy simplificada, es lo que nos permite realmente dibujar en el canvas. Además, le hemos de pasar los puntos que delimitan el polígono y luego podemos pasarle diferentes valores opcionales.

<pre class="language-python"><code>HTML = """&lt;div&gt;&lt;canvas id="cnvs02" width=500 height=433&gt;&lt;/canvas&gt;&lt;/div&gt;"""</code></pre>

<pre class="language-python"><code class="language-python" data-language="python">%%brython -S base -h HTML
fig = Figure('cnvs02', facecolor = "#bbb")
ctx = fig._ctx
width = fig._W
height = fig._H

def triangle(ctx, p1, p2, p3, color = "yellow"):
    x = [p1[0], p2[0], p3[0]]
    y = [p1[1], p2[1], p3[1]]
    Polygon(ctx, x, y, facecolor = color)
    
p1 = [0,height]
p2 = [width, height]
p3 = [width / 2, 0]

triangle(ctx, p1, p2, p3)</code></pre>

[<img class="alignnone size-full wp-image-2868" src="http://pybonacci.org/wp-content/uploads/2014/11/BRYPLOT02.png" alt="BRYPLOT02" width="500" height="433" srcset="https://pybonacci.org/wp-content/uploads/2014/11/BRYPLOT02.png 500w, https://pybonacci.org/wp-content/uploads/2014/11/BRYPLOT02-300x259.png 300w" sizes="(max-width: 500px) 100vw, 500px" />](http://pybonacci.org/wp-content/uploads/2014/11/BRYPLOT02.png)

Como he comentado anteriormente, tenéis más clases y con un poco de maña podéis crear vuestras propias figuras como las que tenéis en el [README del repo](https://bitbucket.org/kikocorreoso/brython-bryplot/src/2de8de16b41b241a295bcd2759ff0c008597dc13/README.md?at=default).

![](https://bytebucket.org/kikocorreoso/brython-bryplot/raw/c49dca54fb12a87d211881a5f1e16e573ec35a49/images/pie.png)

![](https://bytebucket.org/kikocorreoso/brython-bryplot/raw/c49dca54fb12a87d211881a5f1e16e573ec35a49/images/rose.png)

![](https://bytebucket.org/kikocorreoso/brython-bryplot/raw/c49dca54fb12a87d211881a5f1e16e573ec35a49/images/radar.png)

Por último, vamos a dibujar un fractal usando recursión. No voy a explicar el ejemplo y si os hace falta alguna explicación podéis preguntar en los comentarios del blog puesto que este notebook se convertirá en post.

<pre class="language-python"><code>HTML = """&lt;div&gt;&lt;canvas id="cnvs03" width=500 height=433&gt;&lt;/canvas&gt;&lt;/div&gt;"""</code></pre>

<pre class="language-python"><code class="language-python" data-language="python">%%brython -S base -h HTML
from __random import randint

fig = Figure('cnvs03', facecolor = "#bbb")
ctx = fig._ctx
width = fig._W
height = fig._H

def triangle(ctx, p1, p2, p3, color = "yellow"):
    x = [p1[0], p2[0], p3[0]]
    y = [p1[1], p2[1], p3[1]]
    Polygon(ctx, x, y, facecolor = color)
    
def mitad(p1,p2):
    return [abs((p2[0]+p1[0]) / 2.), abs((p2[1]+p1[1]) / 2.)]
    
def sierpinski(ctx, p1, p2, p3, degree):
    if degree &gt; 7:
        raise Exception("Degree should be &lt;= 8")
    COLORS = ('#0000FF', '#008000', '#FF0000', '#00BFBF',
              '#BF00BF', '#BFBF00', '#000000', '#FFFFFF')
    triangle(ctx, p1, p2, p3, color = COLORS[degree])
    if degree &gt; 0:
        sierpinski(ctx, p1, mitad(p1,p2), mitad(p1,p3), degree-1)
        sierpinski(ctx, p2, mitad(p1,p2), mitad(p3,p2), degree-1)
        sierpinski(ctx, p3, mitad(p3,p2), mitad(p1,p3), degree-1)
        
p1 = [0,0]
p2 = [width, 0]
p3 = [width / 2, height]
sierpinski(ctx, p1, p2, p3, 6)</code></pre>

[<img src="http://pybonacci.org/wp-content/uploads/2014/11/BRYPLOT03.png" alt="BRYPLOT03" width="500" height="433" class="alignnone size-full wp-image-2867" srcset="https://pybonacci.org/wp-content/uploads/2014/11/BRYPLOT03.png 500w, https://pybonacci.org/wp-content/uploads/2014/11/BRYPLOT03-300x259.png 300w" sizes="(max-width: 500px) 100vw, 500px" />](http://pybonacci.org/wp-content/uploads/2014/11/BRYPLOT03.png)

Y eso es todo por hoy.

¿Nos vemos en la PyConES?

P.D.: Cómo siempre, tenéis el notebook [aquí](https://github.com/Pybonacci/notebooks).