---
title: 157 cosas de IPython que no sabías y nunca preguntaste (II)
date: 2014-01-29T06:30:53+00:00
author: Kiko Correoso
slug: 157-cosas-de-ipython-que-no-sabias-y-nunca-preguntaste-ii
tags: ipynb, ipython, notebook

En la [primera entrega](https://pybonacci.org/2014/01/24/157-cosas-de-ipython-que-no-sabias-y-nunca-preguntaste-i/) vimos como usar la ayuda de IPython y como personalizar nuestras propias funciones mágicas de ayuda.

En esta segunda entrega vamos a hablar del uso de la historia dentro de IPython.

[Inciso: Os recomiendo que veáis lo que viene a continuación en el [notebook](https://github.com/Pybonacci/notebooks) o en 
[nbviewer](http://nbviewer.ipython.org/).]

IPython guarda la historia de los comandos que se usan en cada línea/celda 
de cada sesión bajo un determinado perfil. Esta información se guarda en 
una base de datos sqlite. Por defecto, se guardan el inicio y fin de 
sesión, los comandos usados en cada sesión y algunos metadatos más. 
IPython también se puede configurar para que almacene los outputs.

# Historia

La base de datos con la historia se guarda en la carpeta que obtenéis haciendo lo siguiente:

```python
from IPython.utils import path
path.locate_profile()
```

```bash
'/home/kiko/.config/ipython/profile_default'
```

Y la base de datos se guardará en esa carpeta con el nombre history.sqlite.

Una forma alternativa de obtener la ruta a la historia bajo el perfil 
actual es usando lo siguiente:

```python
get_ipython().history_manager.hist_file
```

```bash
'/home/kiko/.config/ipython/profile_default/history.sqlite'
```

# Acceso a determinadas celdas de la historia

Para reusar comandos ya usados podemos hacer uso de la **historia** que 
guarda IPython en cada sesión.

  * Podemos usar las teclas de cursor hacia arriba o hacia abajo para recorrer los últimos comandos usados (esto no funciona en el notebook pero sí en la consola de IPython).
  * Si escribimos algo en la línea de comandos y pulsamos el cursor hacia arriba nos mostrará solo lo que comience por lo ya escrito en la línea de comandos (nuevamente, esto no funciona en el notebook pero sí en la consola de IPython).
  * En las sesiones interactivas, el _input_ y el _output_ se guarda en las variables **In** y **Out**. Poniendo el índice de la línea usada nos volverá a ejecutar esa línea, en el caso de que usemos la variable **In** o nos mostrará el _output_ en caso de que usemos la variable **Out**. **In** es una lista mientras que **Out** es un diccionario. En el caso de que no haya _output_ para un número de línea nos dará un **KeyError**. Por ejemplo, veamos las siguientes celdas de código:

```python
In?
```

Nos mostrará en pantalla lo siguiente (esto puede variar en función de 
lo que hayáis escrito previamente en la consola o el notebook, lo 
siguiente solo sirve como ejemplo):

```python
Type:       list
String Form:['', "get_ipython().magic('pinfo In')", "get_ipython().magic('pinfo In')"]
 Length:     3
 Docstring:
list() -> new empty list
list(iterable) -> new list initialized from iterable's items
```

Mientras que si hacemos lo mismo para **Out** obtendremos la siguiente 
info (esto puede variar en función de lo que hayáis escrito previamente 
en la consola o el notebook, lo siguiente solo sirve como ejemplo):

```python
Type:       dict
String Form:{}
Length:     0
Docstring:
dict() -> new empty dictionary
dict(mapping) -> new dictionary initialized from a mapping object's
    (key, value) pairs
dict(iterable) -> new dictionary initialized as if via:
d = {}
for k, v in iterable:
    d[k] = v
dict(**kwargs) -> new dictionary initialized with the name=value pairs
    in the keyword argument list.  For example:  dict(one=1, two=2)
```

Si ahora hacemos lo siguiente:

```python
a = 2
print(a)
```

Nos mostrará un **2** en pantalla pero no lo guarda en el _Output_ 
puesto que solo es visualización. Por tanto, lo siguiente:

```python
Out
```

Nos mostrará (esto puede variar en función de lo que hayáis escrito 
previamente en la consola o el notebook, lo siguiente solo sirve como ejemplo):

```python
{1: '/home/kiko/.config/ipython/profile_default',
 2: '/home/kiko/.config/ipython/profile_default'}
```

Vemos que en **Out** se encuentra lo que hemos obtenido en las primeras 
celdas de código. Si ahora queremos ver otro _output_ podemos hacer lo siguiente:

```python
a
```

Y, como no lo hemos mostrado con un `print`, se añade al _Output_.

```python
Out
```

```python
{1: '/home/kiko/.config/ipython/profile_default',
 2: '/home/kiko/.config/ipython/profile_default/history.sqlite',
 7: 2}
```

Vemos que ya tenemos algún valor para el **Out** y ya podremos acceder 
a ese valor por si lo quisiéramos usar en alguna otra celda. Por 
ejemplo, de la siguiente forma:

```python
b = Out[7]
print(b)
```

Nos mostraría **2** en pantalla.

Como el **In** siempre lo tendremos, en lugar de ser un diccionario es 
una lista y podemos acceder al valor de la celda usando el índice de la 
misma. Por ejemplo:

```python
for celda in In:
    print(celda)
```

Nos mostraría lo siguiente (o algo aproximado a lo siguiente):

```python
from IPython.utils import path
path.locate_profile()
get_ipython().history_manager.hist_file
get_ipython().magic('pinfo In')
a = 2
print(a)
Out
a
Out
b = Out[7]
print(b)
for celda in In:
    print(celda)
```

También podemos acceder a los tres últimos _outputs_ de las tres últimas 
celdas usando \_, \\_\_, \_\__, que nos mostrará el _output_ de la 
última, penúltima o antepenúltima celdas usadas, respectivamente.

```python
print('antepenúltima:n', ___, 'nn')
print('penúltima:n', __, 'nn')
print('última:n', _, 'nn')
```

```python
antepenúltima:
 /home/kiko/.config/ipython/profile_default 
penúltima:
 /home/kiko/.config/ipython/profile_default/history.sqlite 
última:
 2
 ```

Si queremos acceder a los _inputs_ de las últimas celdas podemos usar 
algo parecido pero de la siguiente forma, \_i, \_ii o _iii para la 
última, penúltima o antepenúltima celda de _input_:

```python
print('antepenúltima:n', _iii, 'nn')
print('penúltima:n', _ii, 'nn')
print('última:n', _i, 'nn')
```

```python
antepenúltima:
 print(b) 
penúltima:
 for celda in In:
    print(celda) 
última:
print('antepenúltima:n', ___, 'nn')
print('penúltima:n', __, 'nn')
print('última:n', _, 'nn')
```

Análogamente a lo visto anteriormente, podemos usar __n_ o _i_n_ 
para mostrar, respectivamente, el _output_ o el _input_ de la celda _n_. 
Por ejemplo, para ver el _input_ y el _output_ de la celda anterior (en 
este caso sería la 11) podemos hacer lo siguiente:

```python
print('El input de la celda 11 es:')
print(_i11)
```

Que nos mostrará:

```python
El input de la celda 11 es:
for celda in In:
    print(celda)
```

Y para el _output_:

```python
print('Te he engañado. No existe output para la celda 11')
print('Si intentas acceder al valor _11 obtendrás un NameError ya que no existe la variable')
print('pero te puedo enseñar el de la celda 7:')
print(_7)
```

```python
Te he engañado. No existe output para la celda 11
Si intentas acceder al valor _11 obtendrás un NameError ya que no existe la variable
pero te puedo enseñar el de la celda 7:
2
```

Lo anterior es equivalente a usar **In[n]** o **Out[n]**. Una tercera 
alternativa, además, sería usar **_ih[n]** para los _inputs_ y 
**_oh[n]** para los _outputs_.

```python
In[11]
```

Mostrará:

```python
'for celda in In:n    print(celda)'
```

Mientras que:

```python
_ih[11]
```

Nos mostrará lo mismo:

```python
'for celda in In:n    print(celda)'
```

# Acceso a bloques de historia

Para acceder a toda la historia de la sesión actual podemos usar las 
funciones mágicas **%history** o **%hist**, que es un alias.

Podemos obtener toda la historia o solo una porción. Por ejemplo, el 
siguiente comando nos mostrará la historia desde la celda 1 a la 10 en 
la sesión actual:

```python
%hist 1-10
```

```python
from IPython.utils import path
path.locate_profile()
get_ipython().history_manager.hist_file
In?
a = 2
print(a)
Out
a
Out
b = Out[7]
print(b)
```

Si, además de acceder a las celdas 1 a 10, queremos acceder a celdas 
sueltas podemos usar la siguiente notación para acceder a las celdas 
12 y 14 (además de a las 10 primeras).

```python
%hist 1-10 12 14
```

```python
from IPython.utils import path
path.locate_profile()
get_ipython().history_manager.hist_file
In?
a = 2
print(a)
Out
a
Out
b = Out[7]
print(b)
print('antepenúltima:n', ___, 'nn')
print('penúltima:n', __, 'nn')
print('última:n', _, 'nn')
print('El input de la celda 11 es:')
print(_i11)
```

Si ahora queremos acceder a todas las celdas donde hayamos usado, por 
ejemplo, un comando que incluya 'a = 1' podemos hacer uso de la opción 
**-g** (similar a grep) de la siguiente forma (la salida dependerá de 
vuestra historia):

```python
%hist -g a = 1
```

```python
29/129: a = 1
29/133: a = 1
29/136: a = 1.1
29/138: a = 1
29/142: a = 1.1
29/145: a = 1
29/147: a = 1
29/149: a = 1
29/151: a = 1
51/7: a = 1
185/1: a = 1
187/19: %hist -g a = 1
187/20: %hist -g [a = 1]
187/21: %hist -g a = 1
188/20: %hist -g a = 1
189/2: a = 1
190/1: a = 1
190/3: a = 1
190/4: a = 1
190/10: a = 1
201/1:
code = """
def hello():
    if a = 1:
        print(a)
    elseif a =2:
        print(a)
    else:
        print('kk')
    return None
"""
201/3:
code = """
def hello():
    if a = 1:
        print(a)
    elif a =2:
        print(a)
    else:
        print('kk')
    return None
"""
201/5:
code = """
def hello():
    if a = 1:
        print(a)
    elif a = 2:
        print(a)
    else:
        print('kk')
    return None
"""
201/14:
a = 1
b = exec(code)
201/15:
a = 1
b = exec(code)
print(b)
201/16:
a = 1
b = exec(code)
print(c)
201/17:
a = 1
b = exec(code)
print(b)
201/43: def a():a = 1;return a
201/45: def a():a = 1;b=2return a
201/46: def a():a = 1;b=2;return a,b
201/81:
a = 1
code = """
def hello():
    if a == 1:
        print('a=1')
    elif a == 2:
        print('a=2')
    else:
        if a == 3:
            print('a=3')
    return None
"""
201/85:
a = 1
code = """
def hello():
    if a == 1:
        print('a=1')
    elif a == 2:
        print('a=2')
    else:
        if a == 3:
            print('a=3')
    return None
"""
201/93:
a = 1
code = """
def hello():
    if a == 1:
        return('a=1')
    elif a == 2:
        return('a=2')
    else:
        if a == 3:
            return('a=3')
    return None
"""
201/135:
a = 2
code = """
a = 1
def hello():
    # esto es un comentario de mierda
    if a == 1:
    # esto es otro comentario
        return('a=1 # esto no sería un comentario')
    elif a == 2:
        return('a=2')
    else:
        if a == 3:
            return('a=3')
    return None
hello()
"""
201/157:
a = 2
code = """
a = 1
def hello():
    """Hola"""
    # esto es un comentario de mierda
    if a == 1:
    # esto es otro comentario
        return('a=1 # esto no sería un comentario')
    elif a == 2:
        return('a=2')
    else:
        if a == 3:
            return('a=3')
    return None
class A():
    """Hola"""
    def __init__(self):
        "Hola"
    def _kk(self):
        'Adios'
hello()
help(A)
"""
201/158:
a = 2
code = """
a = 1
def hello():
    '''Hola'''
    # esto es un comentario de mierda
    if a == 1:
    # esto es otro comentario
        return('a=1 # esto no sería un comentario')
    elif a == 2:
        return('a=2')
    else:
        if a == 3:
            return('a=3')
    return None
class A():
    """Hola"""
    def __init__(self):
        "Hola"
    def _kk(self):
        'Adios'
hello()
help(A)
"""
201/159:
a = 2
code = """
a = 1
def hello():
    '''Hola'''
    # esto es un comentario de mierda
    if a == 1:
    # esto es otro comentario
        return('a=1 # esto no sería un comentario')
    elif a == 2:
        return('a=2')
    else:
        if a == 3:
            return('a=3')
    return None
class A():
    "Hola"
    def __init__(self):
        "Hola"
    def _kk(self):
        'Adios'
hello()
help(A)
"""
201/174:
code = """
a = 1
def hello():
    '''
    Hola
    '''
    # esto es un comentario de mierda
    if a == 1:
    # esto es otro comentario
        return('a=1 # esto no sería un comentario')
    elif a == 2:
        return('a=2')
    else:
        if a == 3:
            return('a=3')
    return None
class A():
    "Hola"
    def __init__(self):
        "Hola"
    def _kk(self):
        'Adios'
hello()
help(A)
"""
201/219:
code = """
a = 1
def hello():
    '''
    Hola
    '''
    # esto es un comentario de mierda
    if a == 1:
    # esto es otro comentario
        return('a=1 # esto no sería un comentario')
    elif a == 2:
        return('a=2')
    else:
        if a == 3:
            return('a=3')
    return None
class A():
    "Hola"
    def __init__(self):
        "Hola"
    def _kk(self):
        'Adios'
print(hello())
help(A)
"""
201/230:
code = """
a = 1
def hello():
    '''
    Hola
    '''
    # esto es un comentario de mierda
    if a == 1:
    # esto es otro comentario
        return('a=1 # esto no sería un comentario')
    elif a == 2:
        return('a=2')
    else:
        if a == 3:
            return('a=3')
    return None
class A():
    "Hola"
    def __init__(self):
        "Hola"
    def _kk(self):
        'Adios'
        pass
print(hello())
help(A)
"""
201/233:
code = """
a = 1
def hello():
    '''
    Hola
    '''
    # esto es un comentario de mierda
    if a == 1:
    # esto es otro comentario
        return('a=1 # esto no sería un comentario')
    elif a == 2:
        return('a=2')
    else:
        if a == 3:
            return('a=3')
    return None
class A():
    "Hola"
    def __init__(self):
        "Hola"
    def _kk(self):
        'Adios'
        pass
print(hello())
help(A)
"""
201/237:
code = """
a = 1
def hello():
    '''
    Hola
    '''
    # esto es un comentario de mierda
    if a == 1:
    # esto es otro comentario
        return('a=1 # esto no sería un comentario')
    elif a == 2:
        return('a=2')
    else:
        if a == 3:
            return('a=3')
    return None
class A():
    "Hola"
    def __init__(self):
        "Hola"
        pass
    def _kk(self):
        'Adios'
        pass
print(hello())
help(A)
"""
202/2: a = 1
202/3: a = 1
202/4: a = 1
202/5:
a = 1
print(a)
214/20: %hist -g a = 1
  20: %hist -g a = 1
```

[Gracias a la historia sé que escribo demasiado código estúpido... :-(]

Pero esta busqueda no se restringe a la historia de la sesión actual 
sino que buscará en toda la historia almacenada por IPython bajo el perfil 
que estemos usando. El anterior _output_ indica la sesión, el número de 
línea/celda de esa sesión y el código usado en esa línea/celda con la 
siguiente notación:

_Sesión/celda: Código\_introducido\_en\_la\_celda_

En este caso, podéis ver que en la última línea no se indica el número 
de sesión puesto que se refiere a la sesión actual:

Si usamos la opción **-o** también obtendremos la historia con el 
_output_ incluido. Podéis ver el siguiente ejemplo para ver como funciona:

```python
%hist -o
```

```python
from IPython.utils import path
path.locate_profile()
'/home/kiko/.config/ipython/profile_default'
get_ipython().history_manager.hist_file
'/home/kiko/.config/ipython/profile_default/history.sqlite'
In?
a = 2
print(a)
Out
{1: '/home/kiko/.config/ipython/profile_default',
 2: '/home/kiko/.config/ipython/profile_default/history.sqlite'}
a
2
Out
{1: '/home/kiko/.config/ipython/profile_default',
 2: '/home/kiko/.config/ipython/profile_default/history.sqlite',
 7: 2}
b = Out[7]
print(b)
for celda in In:
    print(celda)
print('antepenúltima:n', ___, 'nn')
print('penúltima:n', __, 'nn')
print('última:n', _, 'nn')
print('antepenúltima:n', _iii, 'nn')
print('penúltima:n', _ii, 'nn')
print('última:n', _i, 'nn')
print('El input de la celda 11 es:')
print(_i11)
print('Te he engañado. No existe output para la celda 11')
print('Si intentas acceder al valor _11 obtendrás un NameError ya que no existe la variable')
print('pero te puedo enseñar el de la celda 7:')
print(_7)
In[11]
'for celda in In:n    print(celda)'
_ih[11]
'for celda in In:n    print(celda)'
%hist 1-10
%hist 1-10 12 14
%hist -g a = 1
%hist -o
```

Otra cosa interesante es la opción **-p**, que coloca un _prompt_ 
delante de cada línea de la historia que se muestra. Esto puede ser 
útil para, por ejemplo, escribir _doctests_.

En el siguiente ejemplo vamos a usar la opción _-p_ junto con la opción _-o_:

```python
%hist -po 1-10
```

```python
>>> from IPython.utils import path
... path.locate_profile()
...
'/home/kiko/.config/ipython/profile_default'
>>> get_ipython().history_manager.hist_file
'/home/kiko/.config/ipython/profile_default/history.sqlite'
>>> In?
>>> a = 2
>>> print(a)
>>> Out
{1: '/home/kiko/.config/ipython/profile_default',
 2: '/home/kiko/.config/ipython/profile_default/history.sqlite'}
>>> a
2
>>> Out
{1: '/home/kiko/.config/ipython/profile_default',
 2: '/home/kiko/.config/ipython/profile_default/history.sqlite',
 7: 2}
>>> b = Out[7]
>>> print(b)
```

Si queremos guardar la historia o parte de la historia en un fichero 
para, por ejemplo, los _doctests_, podemos usar la opción **-f**.

Con la siguiente línea de código vamos a guardar el _input_, el 
_output_ y vamos a colocar la línea del _prompt_ de las 10 primeras 
celdas en un fichero llamado **kk.txt**:

```python
%hist 1-10 -pof kk.txt
```

Si queremos acceder a la historia de una sesión anterior podemos usar lo siguiente:

```python
%hist ~1/1-10
```

```python
from IPython.utils import path
path.locate_profile()
get_ipython().history_manager.hist_file
In?
a = 2
print(a)
Out
a
Out
b = Out[7]
print(b)
```

De esta forma accederemos a las 10 primeras líneas de la sesión anterior. 
Si queremos acceder a las 10 primeras líneas de la penúltima sesión podemos hacer:

```python
%hist ~2/1-10
```

```python
from IPython.utils import path
path.locate_profile()
get_ipython().history_manager.hist_file
In?
a = 2
print(a)
Out
a
Out
b = Out[9]
```

Si, además, queréis numerar las celdas usadas podéis usar la opción **-n**:

```python
%hist ~2/1-10 -n
```

```python
213/1:
from IPython.utils import path
path.locate_profile()
213/2: get_ipython().history_manager.hist_file
213/3: In?
213/4: a = 2
213/5: print(a)
213/6: Out
213/7: a
213/8: Out
213/9: b = Out[9]
```

Algunos de los comandos usados no son aceptados por un intérprete 
Python cualquiera, como por ejemplo los comandos mágicos que empiezan 
por **%**. Por ello, podemos obtener los comandos ya traducidos a código 
Python ejecutable usando la opción **-t** de la historia:

```python
%hist 1-10 -t
```

```python
from IPython.utils import path
path.locate_profile()
get_ipython().history_manager.hist_file
get_ipython().magic('pinfo In')
a = 2
print(a)
Out
a
Out
b = Out[7]
print(b)
```

En la tercera línea podéis ver que en lugar de escribir **%pinfo In** 
ha escrito **get_ipython().magic('pinfo In')**.

# Acceso a la historia de los directorios usados

**_dh** (también podemos usar **%dhist**) nos da información de los 
directorios recorridos. Por ejemplo, voy a recorrer varios directorios y 
después veremos la historia de los directorios recorridos:

```python
cd /home/kiko/pyprojs
```

```python
/home/kiko/pyprojs
```

```python
pwd
```

```python
'/home/kiko/pyprojs'
```

```python
cd /home/kiko/pyprojs/ipython-master/nb/
```

```python
/home/kiko/pyprojs/ipython-master/nb
```

Si ahora escribimos:

```python
%dhist
```

```python
Directory history (kept in _dh)
0: /home/kiko/pyprojs/ipython-master/nb
1: /home/kiko/pyprojs
2: /home/kiko/pyprojs/ipython-master/nb
```

O algo, más o menos, equivalente:

```python
_dh
```

En este caso nos devuelve una lista:

```python
['/home/kiko/pyprojs/ipython-master/nb',
 '/home/kiko/pyprojs',
 '/home/kiko/pyprojs/ipython-master/nb']
```

Si solo quiero saber el directorio del que partí en la sesión de 
IPython en la que me encuentro puedo hacer lo siguiente:

```python
_dh[0]
```

Y obtengo:

```python
'/home/kiko/pyprojs/ipython-master/nb'
```

Y esto es todo de momento. Podéis combinar muchas cosas de las vistas 
aquí con cosas como %macro, %edit, %pastebin,... Si da tiempo, algo muy 
caro últimamente, hablaremos sobre algunas cosas que se me ocurren en 
próximas entregas.

Saludos y hasta la próxima entrega.

P.D.: Si veis alguna errata podéis usar los comentarios o mandar algún 
commit [al repositorio de los notebooks](https://github.com/Pybonacci/notebooks).
