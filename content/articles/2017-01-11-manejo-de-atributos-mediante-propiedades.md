---
title: Manejo de atributos mediante propiedades.
date: 2017-01-11T09:34:12+00:00
author: Alberto Cuevas
slug: manejo-de-atributos-mediante-propiedades
tags: atributos, deletter, getter, property, propiedades, python, setter

En _Python_, cuando creamos una clase, definimos una serie de _atributos_ (que indicarán su estado) y de _métodos_ (que marcarán su comportamiento). El acceso a ambos se realiza de manera sencilla mediante el _operador punto_. Un ejemplo de ello (como nota decir que todo el código mostrado en esta entrada está escrito en _Python 3_ sobre el _IDE PyScripter_)  es el siguiente:

<pre>class MiClase:
    def __init__(self, midato):
        self.dato = midato
    def cuadrado(self):
        return self.dato ** 2
a = MiClase(12.72)
print("El cuadrado es:", a.cuadrado())
a.dato = 7.72
print("El cuadrado es:", a.cuadrado())</pre>

La salida sería:

<pre>&gt;&gt;&gt; 
El cuadrado es: 161.79840000000002
El cuadrado es: 59.5984
&gt;&gt;&gt;</pre>

Para ejemplos sencillos podría ser suficiente actuar de esta manera, pero en otros momentos necesitaremos más versatilidad. Imaginemos que queremos validar los atributos con una determinada condición. En nuestro caso podría ser que los valores de _dato_ estuviesen entre 0 y 10. A los valores menores que 0 se les asignaría el 0 y a los mayores de 10, el 10. Todo ello se lograría fácilmente creando un método que manejase esa condición y ejecutándolo también en _\_\_init\_\_()_:

<pre>class MiClase:
   def __init__(self, midato):
       self.set_dato(midato)
   def set_dato(self, midato):
       if isinstance(midato, (int, float)):
           if midato &lt; 0:
               self.dato = 0
           elif midato &gt; 10:
               self.dato = 10
           else:
               self.dato = midato
       else:
           raise ValueError("Dato no válido")
   def cuadrado(self):
       return self.dato ** 2
a = MiClase(12.72)
print("El cuadrado es:", a.cuadrado())
a.set_dato(7.72)
print("El cuadrado es:", a.cuadrado())

</pre>

Con salida:

<pre>&gt;&gt;&gt; 
El cuadrado es: 100
El cuadrado es: 59.5984
&gt;&gt;&gt;</pre>

En el método _set_dato()_ hacemos la comprobación que el dato es entero o real. De lo contrario lanzamos una excepción. Con ello nos aseguraríamos que el dato cumple las condiciones que queremos.

De la misma forma que hemos creado un método para manejar la escritura del atributo _dato_ podríamos hacerlo para su lectura. Son los denominados, de forma genérica, métodos _getter_ y _setter_, que nos permiten, respectivamente, obtener o modificar los atributos. El concepto de **encapsulación de datos** incluye, además del uso de estos métodos, el que los atributos sean privados (no accesibles desde fuera de la propia clase), algo que en _Python_ se logra añadiendo un doble guión bajo al nombre del atributo. Tendríamos lo siguiente:

<pre>class MiClase:
    def __init__(self, midato):
        self.set_dato(midato)
    def get_dato(self):
        return self.__dato
    def set_dato(self, midato):
        if isinstance(midato, (int, float)):
            if midato &lt; 0:
                self.__dato = 0
            elif midato &gt; 10:
                self.__dato = 10
            else:
                self.__dato = midato
        else:
            raise ValueError("Dato no válido")
        return None
    def cuadrado(self):
        return self.__dato ** 2
a = MiClase(12.72)
print("El cuadrado es:", a.cuadrado())
a.set_dato(7.72)
print("El cuadrado de", a.get_dato(), "es", a.cuadrado())</pre>

La salida es:

<pre>&gt;&gt;&gt; 
El cuadrado es: 100
El cuadrado de 7.72 es 59.5984
&gt;&gt;&gt;</pre>

En _Python_ es habitual que los atributos que en un principio son simples datos estáticos con el tiempo se conviertan en expresiones a calcular dinámicamente o, como ya hemos visto, haya que validarlos de alguna manera. Si actuamos con métodos _getter_ y _setter_ desde el principio podremos hacer esa nueva implementación sin cambiar la forma en la que accedemos a los datos, pero si lo hemos hecho simplemente mediante el operador punto, estaríamos en una situación delicada. Es para superar este escollo, o conseguir una forma mas _pythónica_ que los métodos _getter_ y _setter_, para lo que se usan las propiedades.

¿Qué son exactamente las propiedades?

Las propiedades son atributos que manejamos mediante métodos _getter_, _setter_ y _deleter_, por lo que podríamos llamarlos "atributos manejados". Podemos considerarlos unos atributos "especiales". En realidad en _Python_ los datos, métodos y propiedades de una clase son todos atributos. Los métodos serían atributos "llamables" y las propiedades atributos "personalizables". La única diferencia entre una propiedad y un atributo estándar es que las primeras pueden invocar código personalizado al ser obtenidas, modificadas o eliminadas. Las propiedades se asocian a los atributos de la clase y, como cualquiera de ellos, son heredados en subclases e instancias. Una propiedad maneja un solo y específico atributo, y siempre harán referencia a los métodos de la clase en la que estén definidas.
  
Por lo tanto, las propiedades parecen atributos estándar, pero al acceder a ellos se lanzan los métodos _getter_, _setter_ o _deleter_ correspondientes. Como éstos métodos reciben el argumento _self_, podremos acceder a todos los elementos de la clase o la instancia (sus atributos y métodos) y hacer uso de ellos.

¿Cuándo usar entonces las propiedades?

Respecto al uso desde el principio de simples métodos _getter_ , _setter_ y _deleter_, las propiedades nos aportan un código mas _pythónico_, siendo mas fácil la lectura y escritura de los atributos. La interfaz es mas homogénea ya que a todo se accede mediante el operador punto.

Respecto al uso de atributos estándar, las propiedades nos dan la posibilidad de incorporar código que se ejecute de forma dinámica cuando intentamos acceder a ellos (para obtenerlos, modificarlos o borrarlos). Imaginemos el caso comentado con anterioridad: tenemos hecho un programa donde accedemos a atributos estándar públicos. Posteriormente necesitamos que esos atributos estándar sean validados con unas determinadas condiciones. Mediante las propiedades lograremos nuestro objetivo sin modificar el formato del código ya escrito, algo que no lograríamos con los métodos.

¿Cómo crear las propiedades?

La función _property()_, integrada en el intérprete, nos permite canalizar la lectura o escritura de los atributos (además de interceptar el momento en el que son borrados o proporcionar documentación sobre ellos) mediante funciones o métodos. Su formato es el siguiente:

<p style="text-align: center">
  <span style="color: #666699">atributo_de_clase </span>= <span style="color: #3366ff">property</span>(<span style="color: #339966">fget</span>=None, <span style="color: #800080">fset</span>=None,<span style="color: #ff6600">fdel</span>=None, <span style="color: #ff00ff">doc</span>)
</p>

Ninguno de los parámetros es obligatorio. Si no los pasamos su valor por defecto es _None_. La función _fget()_ se encargará de interceptar la lectura del atributo, la _fset()_ de hacerlo cuando se escriba, la _fdel()_ a la hora de borrarlo y el argumento _doc_ recibirá una cadena para documentar el atributo (si no lo recibe, se copia el docstring de fget(),que por defecto tiene valor _None_). Si alguna operación no está permitida(por ejemplo si intentamos borrar un atributo, algo no demasiado habitual, y no tenemos indicada _fdel()_) se lanzará una excepción. La función _fget()_ devolverá el valor procesado del atributo y tanto _fset()_ como _fdel()_ devolverán _None_. La función _property()_ devuelve un objeto de tipo propiedad que se asigna al nombre del atributo. Un primer ejemplo del uso de las propiedades podría ser el siguiente:

<pre>class Persona:
    def __init__(self, nombre):
        self.set_nombre(nombre)
    def get_nombre(self):
        try:
            print("Pedimos atributo:")
            return self.__nombre
        except AttributeError:
            print("Error. No existe el atributo indicado")
        except:
            print("Error al acceder al atributo")
    def set_nombre(self, nuevo_nombre):
        print("Asignamos el valor", nuevo_nombre,"al atributo 'nombre'")
        self.__nombre = nuevo_nombre
        return None
    def del_nombre(self):
        try:
            print("Borramos atributo", self.__nombre)
            del self.__nombre
        except AttributeError:
            print("Error. No existe el atributo que desea borrar")
        except:
            print("Error al intentar borrar el atributo")
        return None
    nombre = property(get_nombre, set_nombre, del_nombre, "Mi información")
def main():
    a = Persona("Pepe")
    a.nombre = "Juan"
    print(a.nombre)
    del a.nombre
    del a.nombre
    print(a.nombre)
    a.nombre = "Elena"
    print(a.nombre)
    print(help(Persona.nombre))
main()</pre>

Obtenemos la siguiente salida:

<pre>&gt;&gt;&gt; 
Asignamos el valor Pepe al atributo 'nombre'
Asignamos el valor Juan al atributo 'nombre'
Pedimos atributo:
Juan
Borramos atributo Juan
Error. No existe el atributo que desea borrar
Pedimos atributo:
Error. No existe el atributo indicado
None
Asignamos el valor Elena al atributo 'nombre'
Pedimos atributo:
Elena
Help on property:
    Mi información
None
&gt;&gt;&gt;</pre>

En él se ha creado una clase _Persona_ con un atributo privado _nombre_ y tres métodos de tipo _getter_, _setter_ y _deleter_. Posteriormente se crea, mediante la función _property()_, la propiedad _nombre_ vinculada a ellos, que reemplaza al atributo del mismo nombre. Se añade además una información de ayuda. Más adelante creamos una instancia de _Persona_ a la que posteriormente cambiamos el atributo _nombre,_ tras lo cual lo borramos. Al intentar  borrarlo de nuevo, generamos un error que manejamos. También se lanza un error manejado al intentar leer el atributo borrado. Es interesante ejecutar el código paso a paso para ver su funcionamiento exacto. En este ejemplo, por simplicidad, no hemos manejado posibles excepciones en el método _setter_, pero sería conveniente hacerlo en un código completo.

Si no quisiésemos contravenir uno de los principios del _Zen_ de _Python_ ("Debería haber una, y preferiblemente solo una, forma obvia de hacer las cosas") los métodos _get_nombre()_, _set_nombre()_ y _del_nombre()_ deberían ser privados (algo que nuevamente logramos colocando un doble guión bajo antes de su nombre).

Pero tampoco es ésta la forma mas _pythónica_ para tratar con las propiedades, algo que se consigue mediante el uso de _decoradores_. Recordemos que un decorador es básicamente una función que "envuelve" a otra dotándola (al añadir código) de alguna funcionalidad extra. El formato es el siguiente:

<pre>def mifunción(argumentos):
    ...
mifunción = decorador(mifunción)</pre>

También podríamos ponerlo así:

<pre>@decorador
def mifunción(argumentos)
    ...</pre>

Podemos ahora usar la función _property()_ como decorador para que se ejecute cuando queramos acceder a uno de los atributos.

<pre>class Miclase:
    def mi_atributo(self):
        ...
    mi_atributo = property(mi_atributo)</pre>

O también colocarlo de la siguiente manera:

<pre>class Miclase:
     @property
     def mi_atributo(self):
         ...</pre>

De esta manera lograríamos pasar _mi_atributo_ como el primer argumento de la función _property()_, que es el que se usa cuando intentamos leer. El objeto propiedad tiene métodos _getter_, _setter_ y _deleter_ que asignan los métodos de acceso de la propiedad y que devuelven una copia de la propia propiedad. Los podemos, a su vez, usar para decorar métodos con el mismo nombre _mi_atributo_ que usaremos en el momento en que intentamos modificar o borrar el atributo. Es un poco lioso, por lo que el código nos puede aclarar un poco las cosas:

<pre>class Persona:
    def __init__(self, nombre):
        self.nombre = nombre
    @property
    def nombre(self):
        "Documentación del atributo 'nombre' "
        try:
            print("Pedimos atributo:")
            return self.__nombre
        except AttributeError:
            print("Error. No existe el atributo indicado")
        except:
            print("Error al leer el atributo")
    @nombre.setter
    def nombre(self, nuevo_nombre):
        print("Asignamos el valor",nuevo_nombre," al atributo 'nombre'")
        self.__nombre = nuevo_nombre
        return None
    @nombre.deleter
    def nombre(self):
        try:
            print("Borramos atributo", self.__nombre)
            del self.__nombre
        except AttributeError:
             print("Error. No existe el atributo que desea borrar")
        except:
             print("Error al borrar atributo")
        return None
def main():
    a = Persona("Pepe")
    a.nombre = "Juan"
    print(a.nombre)
    del a.nombre
    del a.nombre
    print(a.nombre)
    a.nombre = "Jaime"
    print(a.nombre)
    print(help(Persona.nombre))
main()</pre>

Salida:

<pre>&gt;&gt;&gt; 
Asignamos el valor Pepe al atributo 'nombre'
Valor del atributo 'nombre':
Pepe
Asignamos el valor Juan al atributo 'nombre'
Valor del atributo 'nombre':
Juan
Borramos atributo Juan
Error. No existe el atributo que desea borrar
Valor del atributo 'nombre':
Error. No existe el atributo indicado
None
Asignamos el valor Jaime al atributo 'nombre'
Valor del atributo 'nombre':
Jaime
Help on property:
    Documentación del atributo 'nombre'
None
&gt;&gt;&gt;</pre>

En el código definimos en  _\_\_init\_\_() _el atributo _nombre_ como público. Eso nos permitirá que se ejecute, al crear la instancia de _Persona_, el método _setter_ asociado a su propiedad y por tanto añadir el código que creamos conveniente. Nuevamente, por simplicidad, no se ha añadido manejo de excepciones ni condiciones de validación en él. Mediante la función _property()_ decoramos el método _getter_ que tiene el mismo nombre que nuestro atributo, es decir, _nombre_. Una vez hecho ésto, podemos usar los métodos _setter_ y _deleter_ del objeto propiedad para decorar los métodos correspondientes, de nombre _nombre_. Esta si es la forma mas _pythónica_ de tratar las propiedades.

Los métodos _getter_ de las propiedades pueden ser muy útiles si necesitamos calcular atributos sobre la marcha teniendo como base otros atributos. O también si queremos almacenar el resultado de un cálculo complejo para que sucesivas peticiones de ese cálculo no lo realicen de nuevo, sino que recuperen el resultado previo. Un ejemplo heterodoxo del uso de todo ello  es el siguiente: imaginemos que queremos crear una clase que almacene uno o una serie de valores. Podemos tener  o un número(entero o real) o una lista de números (reales y/o enteros). Como condición de validación tendremos que el número o números esté/n entre 0 y 10 (inclusive). De no ser así asignaremos al número el valor 0. Hay en la clase una propiedad llamada que simula (mediante el uso del módulo _time_) una operación pesada computacionalmente aplicada a los datos. Simulamos que nos cuesta tres segundos calcularla y el resultado es 123.79382.  Lo almacenamos en _transformada_  por si hay una posterior petición de su cálculo. Otra propiedad llamada _media_ calcula el promedio de los datos ya filtrados mediante la validación. Se comprueba que los datos de entrada son correctos y si no se lanza una excepción de tipo _ValueError_.

El código y su correspondiente salida serían algo así, aconsejando una ejecución paso a paso para observar su funcionamiento detalladamente:

<pre>import time
class MiClase:
   def __init__(self, valor=None):
       self.valor = valor
       self.__transformada = None
   @property
   def valor(self):
       return self.__valor
   @valor.setter
   def valor(self, mivalor):
       if isinstance(mivalor, (int, float)):
           if 0 &lt;= mivalor &lt;=10:
               self.__valor = mivalor
           else:
               self.__valor = 0
       elif isinstance(mivalor, list):
           res = []
           for midato in mivalor:
               if isinstance(midato, (int, float)):
                   if 0 &lt;= midato &lt;=10:
                       res.append(midato)
                   else:
                       res.append(0)
               else:
                   raise ValueError ("El dato introducido no es válido")
           self.__valor = res
       else:
           raise ValueError("El dato introducido no es válido")
       return None
    @property
    def transformada(self):
        if not self.__transformada:
            print("Calculando transformada...")
            time.sleep(3)
            self.__transformada = 123.79382
        else:
            print("Transformada en caché. Valor:")
        return self.__transformada
    @property
    def media(self):
        if isinstance(self.valor, list):
            return sum(self.__valor) / len(self.__valor)
        else:
            return "\nNo se puede calcular la media al no ser una lista"
def main():
    datos = [12.21, 8.68, -2, 7.77]
    print("Los datos introducidos son: ", datos)
    a = MiClase(datos)
    print("Los datos filtrados son: ", a.valor)
    print("La media de los datos filtrados es:", a.media)
    print(a.transformada)
    print(a.transformada)
main()
</pre>

<pre>&gt;&gt;&gt; 
Los datos introducidos son: [12.21, 8.68, -2, 7.77]
Los datos filtrados son: [0, 8.68, 0, 7.77]
La media de los datos filtrados es: 4.1125
Calculando transformada...
123.79382
Transformada en caché. Valor:
123.79382
&gt;&gt;&gt; 
</pre>