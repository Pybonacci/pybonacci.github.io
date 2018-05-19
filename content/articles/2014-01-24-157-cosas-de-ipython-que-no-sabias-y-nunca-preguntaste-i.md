---
title: 157 cosas de IPython que no sabías y nunca preguntaste (I)
date: 2014-01-24T06:30:55+00:00
author: Kiko Correoso
slug: 157-cosas-de-ipython-que-no-sabias-y-nunca-preguntaste-i
tags: ipynb, ipython, notebook

Voy a inaugurar una nueva serie de entradas dedicadas a IPython hablando 
de cosas que no son tan evidentes o que la gente no suele usar pero que 
están ahí y son tremendamente útiles una vez que las conoces y las 
incluyes en tu flujo de trabajo.

Inicialmente se iba a llamar _'305928 cosas sobre IPython que no sabías 
(o sí) y que nunca tuviste tiempo de preguntar o de leer en la 
documentación o de leer en el código o nunca te hicieron falta o te 
estabas tomando unas cañas o estabas haciendo otras cosas más seductoras 
e inconfesables o {0}'_ pero me pareció un título un poco largo. 
Finalmente, lo he reducido a 157 y pico, más o menos, para vuestra salud 
mental y la mia. El nombre está inspirado de forma muy libre en el 
nombre de la charla dada por Victor Terrón en la PyConES 2013 (¿que no 
la has visto? venga, a hacer los deberes, rápido. Y después vuelve por aquí).

Primero de todo, **[mode taliban ON]** se escribe IPython, las dos 
primeras en mayúscula y no iPython o ipython o aipaizon o IPhyton (sic) 
**[mode taliban OFF]**. Por tanto, recordadlo si no queréis que la vena 
de la frente de <a href="http://twitter.com/MBussonn" target="_blank">Mathias Bussonier</a> se hinche.

Todos sabéis lo que es IPhyton (:-)), si no es así le puedes echar un 
vistazo a la documentación que está en la <a href="http://www.ipython.org" target="_blank">página oficial</a> o 
visitar este <a href="http://www.youtube.com/watch?v=H6dLGQw9yFQ" target="_blank">vídeo</a> que 
preparó JuanLu sobre el notebook. Si, aun así, sois tan vagos como yo y 
no queréis ver nada de lo anterior os cuento, como brevísimo resumen, 
que IPython es una consola interactiva con super poderes y magia negra incluida.

# Ayuda

## Ayuda estándar de IPython

Vamos a empezar con cosas muy sencillas como el uso de la ayuda que ofrece 
IPython. Normalmente, para obtener ayuda de un objeto se usa el comando 
`help()`, en IPython se puede usar la ayuda usando símbolos de 
interrogación. Si se usa un solo símbolo de interrogación se obtiene 
información general del objeto mientras que si se usan dos símbolos de 
interrogación se puede acceder a la implementación misma del objeto 
(solo en el caso de que haya sido programado en Python). Por ejemplo, 
veamos la ayuda del objeto `calendar` dentro de la biblioteca `calendar` 
disponible en la librería estándar y programada en Python.

```python
from calendar import calendar
?calendar
```

Nos daría la siguiente información (os saltará una ventana en la parte 
inferior del navegador):

```python
Type:       method
String Form:&lt;bound method TextCalendar.formatyear of &lt;calendar.TextCalendar object at 0xb6b6082c&gt;&gt;
File:       /usr/local/lib/python3.3/calendar.py
Definition: calendar(self, theyear, w=2, l=1, c=6, m=3)
Docstring:  Returns a year's calendar as a multi-line string.
Class Docstring:
method(function, instance)
Create a bound instance method object.
```

**[Nota] El comando anterior es equivalente a hacer `calendar?` y 
también es equivalente a usar `%pinfo calendar`.**

Si ahora usamos el doble signo de interrogación obtendremos información 
mucho más detallada como el fichero en el que se encuentra la función y 
el código usado para implementarla, entre otras cosas:

```python
??calendar
```

La siguiente información saldrá en una ventana en la parte inferior del navegador

```python
Type:       method
String Form:&lt;bound method TextCalendar.formatyear of &lt;calendar.TextCalendar object at 0xb6b6082c&gt;&gt;
File:       /usr/local/lib/python3.3/calendar.py
Definition: calendar(self, theyear, w=2, l=1, c=6, m=3)
Source:
    def formatyear(self, theyear, w=2, l=1, c=6, m=3):
        """
        Returns a year's calendar as a multi-line string.
        """
        w = max(2, w)
        l = max(1, l)
        c = max(2, c)
        colwidth = (w + 1) * 7 - 1
        v = []
        a = v.append
        a(repr(theyear).center(colwidth*m+c*(m-1)).rstrip())
        a('n'*l)
        header = self.formatweekheader(w)
        for (i, row) in enumerate(self.yeardays2calendar(theyear, m)):
            # months in this row
            months = range(m*i+1, min(m*(i+1)+1, 13))
            a('n'*l)
            names = (self.formatmonthname(theyear, k, colwidth, False)
                     for k in months)
            a(formatstring(names, colwidth, c).rstrip())
            a('n'*l)
            headers = (header for k in months)
            a(formatstring(headers, colwidth, c).rstrip())
            a('n'*l)
            # max number of weeks for this row
            height = max(len(cal) for cal in row)
            for j in range(height):
                weeks = []
                 for cal in row:
                    if j &gt;= len(cal):
                        weeks.append('')
                    else:
                        weeks.append(self.formatweek(cal[j], w))
                a(formatstring(weeks, colwidth, c).rstrip())
                a('n' * l)
        return ''.join(v)
Class Docstring:
method(function, instance)
Create a bound instance method object.
```

**[Nota] El comando anterior es equivalente a hacer `calendar??` y 
también es equivalente a usar `%pinfo2 calendar`.**

Si ahora usamos la ayuda usual disponible, función `help()` de la 
siguiente forma `help(calendar)`, veremos que la información es bastante 
más escueta que la obtenida mediante IPython.

```python
help(calendar)
```

El resultado será:

```python
Help on method formatyear in module calendar:
formatyear(self, theyear, w=2, l=1, c=6, m=3) method of calendar.TextCalendar instance
Returns a year's calendar as a multi-line string.
```

## Uso de _wildcards_ o comodines

Con el signo de interrogación también podemos usar _wildcards_ para 
obtener todos los objetos que cumplen el criterio. Por ejemplo, nos 
acordamos que el otro día usamos una función que empezaba por _ca_ pero 
no nos acordamos del nombre completo. Podemos buscar todos los objetos 
que se encuentran en el _namespace_ de la siguiente forma:

```python
ca*?
```

Y IPython nos dará lo siguiente:

```python
calendar
callable
```

Esto no es excesivamente útil ya que IPython ofrece autocompletado con 
la tecla de tabulación y llegaríamos al mismo resultado de forma sencilla. 
Pero, ¿y si nos acordamos que el objeto usado terminaba por _ar_ en 
lugar de empezar por _ca_? En este caso, el autocompletado no nos 
resultaría de mucha ayuda. Pero podríamos usar lo siguiente:

```python
*ar?
```

Lo anterior nos daría lo siguiente:

```python
calendar
```

Pero no, no era lo que buscaba. En realidad estaba buscando un objeto 
que contenía `ar`. Lo podemos buscar de la siguiente forma.

```python
*ar*?
```

Lo anterior nos daría lo siguiente:

```python
BytesWarning
DeprecationWarning
FutureWarning
ImportWarning
KeyboardInterrupt
PendingDeprecationWarning
ResourceWarning
RuntimeWarning
SyntaxWarning
UnicodeWarning
UserWarning
Warning
bytearray
calendar
vars
```

## Algunas funciones mágicas de ayuda

También le podéis echar un ojo a `%pdef`, `%pdoc`, `%psource` o 
`%pfile` para obtener información de diverso tipo sobre el `objeto` de turno.

## Creación de nuestras propias funciones mágicas de ayuda

La ayuda del notebook sale en una zona inferior de la ventana del 
navegador. En general me resulta más incómoda que si se imprimiese como 
un ouput estándar dentro del navegador mismo. Con la siguiente receta, 
un poco modificada por mí, podemos hacer que determinada información salga _inline_:

<a href="https://gist.github.com/jiffyclub/5385501" target="_blank">Receta hecha por jiffyclub</a>

```python
# Importamos distintas funciones del módulo oinspect de IPython.
# Muchas de estas funciones son un wrapper sobre las funciones del
#   módulo inspect de la stdlib.
from IPython.core.oinspect import (getsource, getdoc,
                                   find_file, find_source_lines)
# Importamos lo siguiente para mostrar la información en pantalla
from IPython.display import display, HTML
# Importamos lo siguiente para convertir nuestra ayuda a magig functions
from IPython.core.magic import Magics, magics_class, line_magic
# Los siguientes imports serán usados para resaltar la sintáxis del código
#   fuente.
# Es necesario tener instalada la librería pygments.
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter
# Llamamos a la InteractiveShell y obtenemos el namespace
#   del usuario (user_ns) que es un diccionario con los
#   objetos disponibles
ip = get_ipython()
my_ns = ip.user_ns
@magics_class
class KikoMagic(Magics):
    def __init__(self, shell):
        super(KikoMagic, self).__init__(shell)
    @line_magic
    def kdoc(self, obj):
        """
        Retrieve the info of an object and display this info in an output.
        """
        if obj in my_ns.keys():
            print("Doc info for {}:n".format(obj))
            print(getdoc(my_ns[obj]))
        else:
            print("There is no info for {}".format(obj))
    @line_magic
    def kfile(self, obj):
        """
        Retrieve the file where the object is implemented.
        """
        if obj in my_ns.keys():
            print("{} implemented in file:n".format(obj))
            print(find_file(my_ns[obj]))
        else:
            print("We can't not find the file for {}".format(obj))
    @line_magic
    def ksourceline(self, obj):
        """
        Retrieve the first line in the source file where
        the object is implemented.
        """
        if obj in my_ns.keys():
            print("The implementation of {}".format(obj))
            print("starts at line {}".format(find_source_lines(my_ns[obj])))
            print("in file {}".format(find_file(my_ns[obj])))
        else:
            print("We can't not find the file for {}".format(obj))
    @line_magic
    def ksource(self, obj):
        """
        Retrieve the info and the source of an object and
        display the info in an output.
        """
        formatter = HtmlFormatter(linenos=False, cssclass="source", nobackground=True)
        template = """&lt;/pre&gt;
&lt;style&gt;&lt;!--
{}
--&gt;&lt;/style&gt;
&lt;pre&gt;{}"""
 src = getsource(my_ns[obj])
 html = highlight(src, PythonLexer(), formatter)
 css = formatter.get_style_defs()
 display(HTML(template.format(css,html)))
 @line_magic
 def khelp(self, obj):
 self.kdoc(obj)
 print("")
 self.ksourceline(obj)
 print("")
 self.ksource(obj)
# Registramos las nuevas funciones mágicas para que estén
# disponibles en el nb.
ip.register_magics(KikoMagic)
```

Dos de las funciones mágicas solo funcionarán en el notebook y no en 
la consola de IPython ya que estamos haciendo uso de `display(HTML(...))` y 
la _qtconsole_, por ejemplo, no es capaz de mostrar el código html de 
forma correcta. Ahora usamos las nuevas funciones mágicas que acabamos de crear:

  * **kdoc**

```python
%kdoc calendar
```

Que nos devolverá:

```python
Doc info for calendar:
Returns a year's calendar as a multi-line string.
```

  * **kfile**

```python
%kfile calendar
```

Que nos devolverá:

```python
calendar implemented in file: /usr/local/lib/python3.3/calendar.py
```

  * **ksourceline**

```python
%ksourceline calendar
```

que nos devolverá:

```python
The implementation of calendar starts at line 334 in file /usr/local/lib/python3.3/calendar.py
```

  * **k****source**

```python
%ksource calendar
```

que nos devolverá:

```python
def formatyear(self, theyear, w=2, l=1, c=6, m=3):
        """
        Returns a year's calendar as a multi-line string.
        """
        w = max(2, w)
        l = max(1, l)
        c = max(2, c)
        colwidth = (w + 1) * 7 - 1
        v = []
        a = v.append
        a(repr(theyear).center(colwidth*m+c*(m-1)).rstrip())
        a('n'*l)
        header = self.formatweekheader(w)
        for (i, row) in enumerate(self.yeardays2calendar(theyear, m)):
            # months in this row
            months = range(m*i+1, min(m*(i+1)+1, 13))
            a('n'*l)
            names = (self.formatmonthname(theyear, k, colwidth, False)
                     for k in months)
            a(formatstring(names, colwidth, c).rstrip())
            a('n'*l)
            headers = (header for k in months)
            a(formatstring(headers, colwidth, c).rstrip())
            a('n'*l)
            # max number of weeks for this row
            height = max(len(cal) for cal in row)
            for j in range(height):
                weeks = []
                for cal in row:
                    if j &gt;= len(cal):
                        weeks.append('')
                    else:
                        weeks.append(self.formatweek(cal[j], w))
                a(formatstring(weeks, colwidth, c).rstrip())
                a('n' * l)
        return ''.join(v)</code></pre>

  * **khelp**

<pre><code class="language-python">%khelp calendar
```

Que nos devolverá:

```python
Doc info for calendar:
Returns a year's calendar as a multi-line string.
The implementation of calendar
starts at line 334
in file /usr/local/lib/python3.3/calendar.py
    def formatyear(self, theyear, w=2, l=1, c=6, m=3):
        """
        Returns a year's calendar as a multi-line string.
        """
        w = max(2, w)
        l = max(1, l)
        c = max(2, c)
        colwidth = (w + 1) * 7 - 1
        v = []
        a = v.append
        a(repr(theyear).center(colwidth*m+c*(m-1)).rstrip())
        a('n'*l)
        header = self.formatweekheader(w)
        for (i, row) in enumerate(self.yeardays2calendar(theyear, m)):
            # months in this row
            months = range(m*i+1, min(m*(i+1)+1, 13))
            a('n'*l)
            names = (self.formatmonthname(theyear, k, colwidth, False)
                     for k in months)
            a(formatstring(names, colwidth, c).rstrip())
            a('n'*l)
            headers = (header for k in months)
            a(formatstring(headers, colwidth, c).rstrip())
            a('n'*l)
            # max number of weeks for this row
            height = max(len(cal) for cal in row)
            for j in range(height):
                weeks = []
                for cal in row:
                    if j &gt;= len(cal):
                        weeks.append('')
                    else:
                        weeks.append(self.formatweek(cal[j], w))
                a(formatstring(weeks, colwidth, c).rstrip())
                a('n' * l)
        return ''.join(v)
```

¡¡Eyyy, qué chulo!! Acabamos de personalizar un poco el notebook de IPython de forma muy sencilla.

Si solo queremos hacer una función mágica lo podemos hacer de forma un 
poco más sencilla que la vista anteriormente. En el siguiente código se 
muestra cómo (<a href="https://github.com/ipython/ipython/wiki/Cookbook:-Sending-built-in-help-to-the-pager" target="_blank">receta hecha por Brian Granger</a> y 
que he actualizado a las últimas versiones de IPython para hacerla funcionar):

```python
from IPython.core.oinspect import getdoc
ip = get_ipython()
my_ns = ip.user_ns
# Definimos la función que hace lo que queremos. La siguiente
#   función hace lo mismo que la función mágica kdoc que hemos
#   implementado anteriormente
def new_magic(obj):
    if obj in my_ns.keys():
        print(getdoc(my_ns[obj]))
    else:
        print("No info found for {}".format(obj))
## En la siguiente línea definimos la anterior función como
##   una 'line magic' que se llamará 'my_new_magic'
ip.register_magic_function(new_magic, 'line', "my_new_magic")
```

Ahora la vamos a hacer funcionar:

```python
%my_new_magic calendar
```

que nos devolverá:

```python
Returns a year's calendar as a multi-line string.
```

## Resumen

Hemos visto como:

  * usar la ayuda de IPython, más avanzada que el uso de la función built-in `help()`,
  * uso de comodines (_wildcards_),
  * las funciones mágicas útiles para obtener ayuda de Python,
  * como crear nuestras propias funciones mágicas de ayuda (o de lo que queráis).

Si se os ocurre algo para completar esta información podéis hacer un 
pull request a <a href="https://github.com/Pybonacci/notebooks" target="_blank">nuestro repo 
de notebooks</a> y actualizaremos la información.
