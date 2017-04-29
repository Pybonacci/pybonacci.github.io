---
title: Desarrollo Dirigido por Pruebas en Python (III). Independencia del Sistema
date: 2013-12-03T20:43:49+00:00
author: javierjus
slug: desarrollo-dirigido-por-pruebas-en-python-iii-independencia-del-sistema

En esta entrega continuamos aplicando desarrollo dirigido por pruebas (o Test-Driven Development en inglés) para implementar una aplicación que busque tweets con un hashtag concreto y los guarde en un archivo. En concreto nos centraremos en el código que construye el nombre del fichero con la fecha actual y el hashtag buscado.
  
Nos enfrentaremos con el problema de depender de la fecha del sistema por lo que el resultado esperado de la pruebas cambiará cada día. Para solucionarlo, veremos cómo podemos independizar nuestro código de detalles del sistema y hacerlo más fácil de probar. Esto nos dará pie a presentar los dobles de prueba.
  
Las entregas anteriores de esta serie son:

[Desarrollo dirigido por pruebas en Python (I): Una historia que pasa todos los días](http://pybonacci.org/2013/01/07/desarrollo-dirigido-por-pruebas-en-python-i-una-historia-que-pasa-todos-los-dias/#more-1352 "Desarrollo dirigido por pruebas en Python (I): Una historia que pasa todos los días")

[Desarrollo Dirigido por Pruebas en Python (II). Un Caso Práctico (I)](http://pybonacci.org/2013/06/19/desarrollo-dirigido-por-pruebas-en-python-ii-un-caso-practico-i/ "Desarrollo Dirigido por Pruebas en Python (II). Un Caso Práctico (I)")

Aunque la aplicación es la misma en todas las entregas, en cada una nos centramos en un problema concreto, así que puedes leer esta entrega aunque no hayas leído las dos anteriores.

## **El diario de diseño**

Vamos a recuperar nuestro diario de diseño de la entrega anterior para ver en qué estado se encuentra el desarrollo de nuestra aplicación.

<table border="1" cellspacing="0" cellpadding="0">
  <tr>
    <td valign="top" width="576">
      <b>Diario de diseño.</b>
    </td>
  </tr>
  
  <tr>
    <td valign="top" width="576">
      1) Conectarse a Internet y obtener los mensajes que contengan un tag concreto.<span style="text-decoration:line-through;">2) Procesar los tweets para obtener el nombre y dirección twitter del autor, la fecha y el contenido del tweet.</span></p> 
      
      <p style="padding-left:30px;">
        <span style="text-decoration:line-through;">2.1) Definir el contenido de tweetDePrueba</span>
      </p>
      
      <p style="padding-left:30px;">
        <span style="text-decoration:line-through;">2.2) Los elementos de la lista resultante deben tener el nombre y dirección twitter del autor, la fecha y el contenido del tweet. </span>
      </p>
      
      <p>
        3) Guardar la información anterior en un nuevo fichero
      </p>
      
      <p>
        4) Crear una interfaz de usuario por línea de comandos.</td> </tr> </tbody> </table> 
        
        <p>
          Ya hemos terminado la funcionalidad 2. Ahora podemos elegir la tarea que quieras implementar. Para esta entrada, vamos a elegir la tarea 3. Al igual que hicimos en la entrega anterior, vamos a descomponer esta área en otras más pequeñas:
        </p>
        
        <table border="1" cellspacing="0" cellpadding="0">
          <tr>
            <td valign="top" width="576">
              <b>Diario de diseño.</b>
            </td>
          </tr>
          
          <tr>
            <td valign="top" width="576">
              1) Conectarse a Internet y obtener los mensajes que contengan un tag concreto.<span style="text-decoration:line-through;">2) Procesar los tweets para obtener el nombre y dirección twitter del autor, la fecha y el contenido del tweet.</span>3) Guardarlos tweets procesados en un nuevo fichero</p> 
              
              <p style="padding-left:30px;">
                3.1) Crear el nombre de fichero siguiendo este formato: “año-mes-dia tag.txt”
              </p>
              
              <p style="padding-left:30px;">
                3.2) Cada tweet se guarda en una línea con los valores separados por comas.
              </p>
              
              <p style="padding-left:30px;">
                3.3) Crear el fichero con el nombre y contenido indicados en 3.1 y 3.2
              </p>
              
              <p>
                4) Crear una interfaz de usuario por línea de comandos.</td> </tr> </tbody> </table> 
                
                <p>
                  Como se describe en el diario de diseño, vamos a crear un fichero cuyo nombre contenga la fecha del sistema. A continuación empezamos a implementar nuestra nueva funcionalidad escribiendo pruebas.
                </p>
                
                <h2>
                  <b>La primera prueba</b>
                </h2>
                
                <p>
                  Una vez qué tenemos claro qué vamos a hacer, el primer paso es escribir una prueba para expresar el resultado esperado del código que vamos a escribir. Empezamos generando el nombre adecuado de un fichero y, para ello, escribiremos una prueba que exponga cómo lo queremos obtener.
                </p>
                
                <pre><code class="language-python">class TestTweetsEnFichero(unittest.TestCase):
	def testCreaNombreFichero(self):
		tef = TweetsEnFichero()
		esperado = "2013-03-30 PyConEs.txt"
		self.assertEquals(esperado, tef.crearNombreFichero("PyConEs"))</code></pre>
                
                <p>
                  Para que esta prueba pase, creamos una nueva clase, <em>TweetsEnFichero</em>, que contendrá todo lo necesario para almacenar el contenido de los tweets en un fichero. Suponemos que escribimos y ejecutamos esta prueba el 30/03/2013. La implementación más sencilla para que esta prueba pase es:
                </p>
                
                <pre><code class="language-python">class TweetsEnFichero:
	def crearNombreFichero(self, tag):
		return  "2013-03-30 PyConEs.txt"</code></pre>
                
                <p>
                  Con esta implementación tenemos el código más sencillo que hace que la prueba pase con éxito. Ahora que ya tenemos algo que funciona y que nos muestra cómo trabajar vamos a mejorarlo. Podemos hacer algunas refactorizaciones al código anterior. Por ejemplo, ya que tenemos el hashtag, podemos utilizarlo y comprobar que la prueba sigue funcionando.
                </p>
                
                <pre><code class="language-python">class TweetsEnFichero:
	def crearNombreFichero(self, tag):
		return  "2013-03-30 “+tag+”.txt"</code></pre>
                
                <p>
                  Veamos a continuación cómo podemos independizarnos de la fecha actual.
                </p>
                
                <h2>
                  <b>¡Independencia!... del día y la hora                      </b>
                </h2>
                
                <p>
                  Comenzamos separando la responsabilidad de obtener la fecha darle el formato adecuado del resto del código. Para ello vamos a escribir un nuevo método y nuestro primer paso, lógicamente, será escribir primero la prueba que nos defina qué debe hacer el código que vamos a escribir.
                </p>
                
                <pre><code class="language-python">def testGetFechaActual(self):
		tef = TweetsEnFichero()
		esperado = "2013-03-30"
		self.assertEquals(esperado, tef.getFechaActual())</code></pre>
                
                <p>
                  Una vez que la prueba falla pasamos a la implementación. Veamos el código.
                </p>
                
                <pre><code class="language-python">def getFechaActual(self):
		now = datetime.now()
		return str(now.year) + "-" + str(now.month) + "-" + str(now.day)</code></pre>
                
                <p>
                  Sin embargo con la implementación anterior la prueba falla porque el mes es 3 en vez de 03. Esto también pasará cuando el día sea menor de 10. Como esta prueba no pasa con éxito no podemos dar por terminada la implementación. La solución más rápida es añadir el “0” que falta, como se muestra en el siguiente código.
                </p>
                
                <pre><code class="language-python">def getFechaActual(self):
		now = datetime.now()
		return str(now.year) + "-" + “0” + str(now.month) + "-" + str(now.day)</code></pre>
                
                <p>
                  Ahora la prueba pasa con éxito. Además, hemos descubierto una nueva tarea que necesitamos para que el nombre se genere correctamente, y que añadimos a nuestro diario (tarea 3.4).
                </p>
                
                <table border="1" cellspacing="0" cellpadding="0">
                  <tr>
                    <td valign="top" width="576">
                      <b>Diario de diseño.</b>
                    </td>
                  </tr>
                  
                  <tr>
                    <td valign="top" width="576">
                      1) Conectarse a Internet y obtener los mensajes que contengan un tag concreto.<span style="text-decoration:line-through;">2) Procesar los tweets para obtener el nombre y dirección twitter del autor, la fecha y el contenido del tweet.</span>3) Guardarlos tweets procesados en un nuevo fichero3.1) Crear el nombre de fichero siguiendo este formato: “año-mes-día tag.txt”</p> 
                      
                      <p>
                        3.2) Cada tweet se guarda en una línea con los valores separados por comas.
                      </p>
                      
                      <p>
                        3.3) Crear el fichero con el nombre y contenido indicados en 3.1 y 3.2
                      </p>
                      
                      <p>
                        3.4) Añadir un “0” cuando el mes o el día sean menores de 10.
                      </p>
                      
                      <p>
                        4) Crear una interfaz de usuario por línea de comandos.</td> </tr> </tbody> </table> 
                        
                        <p>
                          Este es un buen momento para refactorizar. Vamos a refactorizar las pruebas para evitar código duplicado. En concreto sacamos la creación del objeto bajo prueba al método <i>setUp</i> tal y como se muestra a continuación.
                        </p>
                        
                        <pre><code class="language-python">class TestTweetsEnFichero(unittest.TestCase):
	def setUp(self):
		self.tef = TweetsEnFichero()
	def testCreaNombreFichero(self):
		esperado = "2013-03-30 PyConEs.txt"
		self.assertEquals(esperado, self.tef.crearNombreFichero("PyConEs"))
	def testGetFechaActual(self):
		esperado = "2013-03-30"
		self.assertEquals(esperado, self.tef.getFechaActual())</code></pre>
                        
                        <p>
                          También refactorizamos el código de la aplicación para que utilice el método <i>getFechaActual</i> en vez de la fecha incrustada como cadena de texto y el parámetro <em>hashtag</em>.
                        </p>
                        
                        <pre><code class="language-python">class TweetsEnFichero:
	def crearNombreFichero(self, hashtag):
		return self.getFechaActual() +" "+ hashtag + ".txt"</code></pre>
                        
                        <p>
                          Podríamos continuar escribiendo pruebas para que el código añada un cero delante del mes y del día cuando haga falta, pero nuestro código aún depende de la fecha actual del sistema (llamada a <i>datetime::now</i>) lo que aumenta la dificultad de implementar esta funcionalidad. Por ello, nuestro siguiente paso será independizarnos de la fecha del sistema.
                        </p>
                        
                        <h2>
                          <b>Funciona hoy, funciona mañana</b>
                        </h2>
                        
                        <p>
                          Las pruebas anteriores solo funcionarán hoy, mañana será otro día, <i>datetime::now</i> devolverá otra fecha y las pruebas fallarán. El problema es que hemos incrustado una dependencia con <i>datetime::now</i> en nuestro código, por lo que depende de la llamada al sistema que devuelve la fecha. Necesitamos una manera de romper esa dependencia para poder controlar el código.
                        </p>
                        
                        <p>
                          El primer paso es refactorizar para proporcionar el <i>datetime</i> a utilizar desde el exterior. El código resultante se muestra a continuación.
                        </p>
                        
                        <pre><code class="language-python">class TweetsEnFichero:
	def __init__(self, timeProvider):
		self.timeProvider = timeProvider
	def getFechaActual(self):
		now = self.timeProvider.now()
		return str(now.year) + "-" + str(now.month) + "-" + str(now.day)</code></pre>
                        
                        <p>
                          Después, modificamos las pruebas que tenemos que usen <i>datetime</i> y todo sigue funcionando. Como al final de la sección anterior refactorizamos el código para evitar el código duplicado, solo hemos tenido que modificar una única línea. Si no hubiéramos refactorizado tendríamos que cambiar todas las pruebas. Recuerda, evitar el código duplicado hace tu código más sencillo de cambiar y mejorar.
                        </p>
                        
                        <pre><code class="language-python">class TestTweetsEnFichero(unittest.TestCase):
	def setUp(self):
		self.tef = TweetsEnFichero(datetime)</code></pre>
                        
                        <p>
                          ;
                        </p>
                        
                        <p>
                          Vamos a continuar modificando las pruebas. Como podemos indicar desde el exterior el encargado de devolver la fecha, podemos crear un “doble” que devuelva siempre la misma fecha. Así podremos saber cuál serán los resultados esperados de la pruebas. Nuestro doble de pruebas se llama <i>DatetimeStub</i> y su misión es reemplazar al <i>Datetime</i> del sistema para devolver siempre la misma fecha. Así, podemos predecir los resultados esperados de la prueba y hacer que no cambien de un día para otro.
                        </p>
                        
                        <pre><code class="language-python">class DatetimeStub ():
	def now(self):
		self.year = 2013
		self.month = 3
		self.day = 29
		return self</code></pre>
                        
                        <p>
                          Los dobles de prueba son un elemento muy poderoso a la hora de escribir pruebas. Al final de este artículo tienes más información sobre dobles. Vamos a modificar la prueba que hemos escrito para utilizar nuestro doble.
                        </p>
                        
                        <pre><code class="language-python">class TestTweetsEnFichero(unittest.TestCase):
	def setUp(self):
		self.tef = TweetsEnFichero(DatetimeStub ())</code></pre>
                        
                        <p>
                          Todas las pruebas siguen funcionando correctamente. Ya estamos independizados de la fecha y hora.
                        </p>
                        
                        <h2>
                          <b>Hazlo pero no me digas cómo</b>
                        </h2>
                        
                        <p>
                          Por comodidad, podemos hacer que, si no se indica ningún <i>datetime</i> concreto, se utilice el <i>datetime</i> del sistema. Vamos a escribir una prueba que lo ponga de manifiesto:
                        </p>
                        
                        <pre><code class="language-python">def testGetFechaActual_DatetimePorDefecto(self):
		self.tef = TweetsEnFichero()
		self.assertEquals(datetime, self.tef.timeProvider)</code></pre>
                        
                        <p>
                          Y ahora implementamos el <em>datetime</em> del sistema por defecto en el constructor  lo utilizamos en el método <i>getFechaActual</i>.
                        </p>
                        
                        <pre><code class="language-python">class TweetsEnFichero:
	def __init__(self, timeProvider = datetime):
		self.timeProvider = timeProvider
	def getFechaActual(self):
		now = self.timeProvider.now()
		return str(now.year) + "-" + "0" + str(now.month) + "-" + str(now.day)</code></pre>
                        
                        <p>
                          Una vez que todo funciona, continuamos con la siguiente funcionalidad.
                        </p>
                        
                        <h2>
                          <b>Un cero a la izquierda</b>
                        </h2>
                        
                        <p>
                          Tenemos pendiente en nuestro diario de diseño añadir un “0” cuando el mes y día sean menores de 10. Vamos a escribir nuevas pruebas que nos empujen a implementar esta funcionalidad, por ejemplo la siguiente:
                        </p>
                        
                        <pre><code class="language-python">def testGetFechaActual_ConMesMayorQue10NoSeIncluyeElCero(self):
		self.tef = TweetsEnFichero(DatetimeStub("12-10-2013"))
		esperado = "2013-10-12"
		self.assertEquals(esperado, self.tef.getFechaActual())</code></pre>
                        
                        <p>
                          Como se ve en la prueba anterior, necesitamos usar otras fechas distintas que la incluida en nuestro doble de pruebas (clase <i>DatetimeStub</i>). Vamos a modificarlo para que pueda aceptar cualquier fecha como se muestra a continuación.
                        </p>
                        
                        <pre><code class="language-python">class DatetimeStub():
	def __init__(self, date = "30-3-2013"):
		fields = date.split("-")
		self.year = int(fields[2])
		self.month = int(fields[1])
		self.day = int(fields[0])
	def now(self):
		return self</code></pre>
                        
                        <p>
                          Recuerda que el código de prueba (casos de prueba, dobles, etc.) debe ser lo más sencillo posible por dos motivos. El primero es que no escribimos pruebas para verificar pruebas (ni dobles) por lo que tienen que ser simples y de pocas líneas para evitar fallos. El segundo es que, cuando haya un error en el código, una o varias pruebas fallarán. Queremos entender rápidamente qué hace la prueba para que nos dirijan hacia el error en el código.
                        </p>
                        
                        <p>
                          Una vez que hemos modificado <i>DatetimeStub</i> y ejecutamos la prueba esta falla, ya que siempre añadimos un “0” delante del mes. Añadimos un if al método <i>getFechaActual</i> y la prueba funciona (veremos este código un poco más adelante).
                        </p>
                        
                        <p>
                          Vamos a escribir una segunda prueba que ponga un 0 delante del día. Esta prueba se muestra a continuación.
                        </p>
                        
                        <pre><code class="language-python">def testGetFechaActual_ConDiaMenorQue10SeIncluyeUnCero(self):
		self.tef = TweetsEnFichero(DatetimeStub("7-10-2013"))
		esperado = "2013-10-07"
		self.assertEquals(esperado, self.tef.getFechaActual())</code></pre>
                        
                        <p>
                          La prueba falla así que podemos añadir más código. Añadimos otro if para controlar si le ponemos el 0 al día y, con eso, todas las pruebas funcionan ya. El método <i>getFechaActual</i> (con el cambio de añadir un 0 al mes y al día) ha quedado así.
                        </p>
                        
                        <pre><code class="language-python">def getFechaActual(self):
		now = self.timeProvider.now()
		month = str(now.month)
		if now.month &lt; 10:
			month = "0" + month
		day = str(now.day)
		if now.day &lt; 10:
			day = "0" + day
		return str(now.year) + "-" + month  + "-" + day</code></pre>
                        
                        <p>
                          Toca refactorizar. Vemos que el código para añadir un 0 es el mismo y que solo cambia el valor (mes o día). Para evitar duplicar el código extraemos un método auxiliar, al que llamamos <i>cadenaDosDigitos</i>, tal y como se muestra a continuación.
                        </p>
                        
                        <pre><code class="language-python">def cadenaDosDigitos(self, num):
		if num &lt; 10:
			return "0" + str(num)
		return  str(num)
	def getFechaActual(self):
		now = self.timeProvider.now()
		return str(now.year)
			   + "-" + self.cadenaDosDigitos(now.month)
			   + "-" + self.cadenaDosDigitos(now.day)</code></pre>
                        
                        <p>
                          Todas las pruebas funcionan por lo que damos por cerrada esta funcionalidad. Repasemos el diario de diseño.
                        </p>
                        
                        <table border="1" cellspacing="0" cellpadding="0">
                          <tr>
                            <td valign="top" width="576">
                              <b>Diario de diseño.</b>
                            </td>
                          </tr>
                          
                          <tr>
                            <td valign="top" width="576">
                              1) Conectarse a Internet y obtener los mensajes que contengan un tag concreto.<span style="text-decoration:line-through;">2) Procesar los tweets para obtener el nombre y dirección twitter del autor, la fecha y el contenido del tweet.</span>3) Guardarlos tweets procesados en un nuevo fichero</p> 
                              
                              <p style="padding-left:30px;">
                                <span style="text-decoration:line-through;">3.1) Crear el nombre de fichero siguiendo este formato: “año-mes-día tag.txt”</span>
                              </p>
                              
                              <p style="padding-left:30px;">
                                3.2) Cada tweet se guarda en una línea con los valores separados por comas.
                              </p>
                              
                              <p style="padding-left:30px;">
                                3.3) Crear el fichero con el nombre y contenido indicados en 3.1 y 3.2
                              </p>
                              
                              <p style="padding-left:30px;">
                                <span style="text-decoration:line-through;">3.4) Añadir un “0” cuando el mes o el día sean menores de 10.</span>
                              </p>
                              
                              <p>
                                4) Crear una interfaz de usuario por línea de comandos.</td> </tr> </tbody> </table> 
                                
                                <p>
                                  Hasta aquí llegamos en esta entrada. En la siguiente escribiremos el código que guarde los tweets en el fichero, ya con el nombre correcto.
                                </p>
                                
                                <h2>
                                  <b>Dobles de prueba</b>
                                </h2>
                                
                                <p>
                                  Para escribir buenas pruebas unitarias rompemos las dependencias de la clase bajo prueba. Así, centramos la prueba en un único fragmento de código y podemos controlar todas sus interacciones con el entorno, como por ejemplo, con la fecha del sistema. Sabremos que, si la prueba falla, el fallo estará en el código bajo prueba, no en el código de los métodos auxiliares. El diseño queda más flexible ya que no incrustamos dependencias con otras clases dentro de nuestro código.
                                </p>
                                
                                <p>
                                  Para conseguir esta independencia, podemos utilizar versiones ficticias de las clases colaboradoras que devuelvan valores predecibles. Con ello podremos definir los resultados esperados para la prueba.  Estas clases ficticias son dobles de prueba (o <i>test doubles</i> en inglés). A veces también se llaman  mocks, fakes, spies pero en la actualidad dichos nombres se utilizan para indicar dobles de prueba con algunas características especiales.
                                </p>
                                
                                <p>
                                  Antes hemos creado nuestro propio doble de prueba (la clase <i>DatetimeStub</i>), pero existen herramientas que nos facilitan la creación e dobles. Para saber más sobre dobles de prueba consulta la sección logro desbloqueado un poco más adelante.
                                </p>
                                
                                <h2>
                                  <b>Conclusiones</b>
                                </h2>
                                
                                <p>
                                  En esta segunda entrega nos hemos encontrado el problema de depender de una característica del sistema que no podíamos controlar, la fecha, y cómo hemos evolucionado nuestro diseño. El código resultante que hemos creado en esta entrada se muestra a continuación
                                </p>
                                
                                <pre><code class="language-python">class TweetsEnFichero:
	def __init__(self, timeProvider = datetime):
		self.timeProvider = timeProvider
	def _getFechaActual(self):
		now = self.timeProvider.now()
		return str(now.year)
			+ "-" + self._cadenaDosDigitos(now.month)
			+ "-" + self._cadenaDosDigitos(now.day)
	def _cadenaDosDigitos(self, num):
		pre = ""
		if num &lt; 10:
			pre = "0"
		return  pre+ str(num)
	def crearNombreFichero(self, hashtag):
		return self._getFechaActual() +" "+ hashtag + ".txt"</code></pre>
                                
                                <p>
                                  Test-Driven Development nos ha ayudado a llegar hasta un mejor diseño al detectar la necesidad de extraer la dependencia del <i>datetime</i> del sistema para poder escribir pruebas. Nos vemos en la próxima entrada.
                                </p>
                                
                                <h2>
                                  <b>Logro desbloqueado</b>
                                </h2>
                                
                                <p>
                                  En este ejemplo hemos creado nuestros propios dobles de prueba, pero existen varias librerías que automatizan este trabajo por nosotros. En Python, a partir de la versión 3.3, incorpora una librería de mocks llamada MagicMocks y que también se puede utilizar de manera independiente. Utilizando esta librería, nuestro ejemplo quedaría de la siguiente manera.
                                </p>
                                
                                <pre><code class="language-python">def testGetFechaActual_ConMesMayorQue10NoSeIncluyeElCero(self):
        datetimeStub = Mock()
        datetimeStub.year = 2013
        datetimeStub.month = 3
        datetimeStub.day = 30
        datetimeStub.now = Mock(return_value=datetimeStub)
        tef = TweetsEnFichero(datetimeStub)
           esperado = "2013-03-30"
        self.assertEquals(esperado, tef.getFechaActual())</code></pre>
                                
                                <p>
                                  Y ya no es necesario crear la clase DatetimeStub. Puedes leer más sobre dobles de prueba y Python en el blog del autor: <a title="Un ejemplo de Mocks en Python (con Mockito y MagicMock)" href="http://iwt2-javierj.tumblr.com/post/36695988608/mocks-en-python-previa-python-tdd">Un ejemplo de Mocks en Python (con Mockito y MagicMock)</a>.  También puedes encontrar más teoría (muy resumida y con ejemplos en Java) sobre el mundo de los dobles de prueba en el libro inconcluso <a title="Desarrollo Dirigido por Pruebas Práctico" href="http://www.iwt2.org/web/opencms/IWT2/comunidad/LibroTDD/?locale=es">Desarrollo Dirigido por Pruebas Práctico</a>. Por último, tienes otro ejemplo de cómo aislarte de la dependencia de la fecha del sistema en Python aquí: <a title="Cómo aislarnos de las dependencias del sistema. Un caso práctico con Python, MagicMock y TDD" href="http://iwt2-javierj.tumblr.com/post/67646801575/como-aislarnos-de-las-dependencias-del-sistema-un-caso">Cómo aislarnos de las dependencias del sistema. Un caso práctico con Python, MagicMock y TDD<br /> </a>
                                </p>