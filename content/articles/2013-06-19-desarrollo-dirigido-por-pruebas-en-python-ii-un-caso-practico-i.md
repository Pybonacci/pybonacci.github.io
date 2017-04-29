---
title: Desarrollo Dirigido por Pruebas en Python (II). Un Caso Práctico (I)
date: 2013-06-19T23:05:49+00:00
author: javierjus
slug: desarrollo-dirigido-por-pruebas-en-python-ii-un-caso-practico-i
tags: python, TDD, test, testing

A principios de año escribimos una entrada que puedes leer [aquí](http://pybonacci.org/2013/01/07/desarrollo-dirigido-por-pruebas-en-python-i-una-historia-que-pasa-todos-los-dias/ "Desarrollo dirigido por pruebas en Python (I): Una historia que pasa todos los días"). Después de un parón más largo de lo previsto, volvemos a la carga con el desarrollo dirigido por pruebas en Python.

Vamos a utilizar TDD y el módulo unittest para crear una aplicación que se conecte a twitter, recupere los mensajes de un hashtag y almacene parte de los mensajes en un fichero. El nombre del fichero será la fecha actual y el hashtag. El fichero contendrá la información de cada tweet separada por comas.

Dividiremos este ejemplo en varias entradas. En cada entrada, desarrollaremos una parte de la aplicación a medida que aprendemos distintas técnicas y buenas prácticas para aplicar TDD. En la primera entrada empezaremos con la aplicación y veremos algunos aspectos clave de la aplicación de TDD.

## **El diario de diseño**

Vamos  comenzar creando el diario de diseño. Este diario es la lista de tareas que tenemos pendientes (una to-do list) de hacer cómo código a escribir o funcionalidad a implementar y nos va a servir para mantenernos en todo momento con el foco centrado. Utilizamos el diario cuando ya tengamos una funcionalidad implementada (y gracias a TDD probada) para decir la siguiente y cuando, durante un ciclo de TDD, se nos ocurra nueva funcionalidad o nuevas condiciones a implementar en nuestro código. Vamos a ver las tareas que tenemos que hacer en el cuadro 1.

<table border="1" cellspacing="0" cellpadding="0">
  <tr>
    <td valign="top" width="576">
      <b>Cuadro 1. Diario de diseño.</b>
    </td>
  </tr>
  
  <tr>
    <td valign="top" width="576">
      1) Conectarse a Internet y obtener los mensajes que contengan un tag concreto.<br /> 2) Procesar los tweets para obtener el nombre y dirección twitter del autor, la fecha y el contenido del tweet.<br /> 3) Guardar la información anterior en un nuevo fichero.<br /> 4) Crear una interfaz de usuario por línea de comandos.
    </td>
  </tr>
</table>

Para empezar a escribir código elegimos una de las tareas anteriores, la que queramos. No tenemos que imponernos un orden ni pensar que tenemos dependencias. En su lugar elegimos la tarea que consideremos más importante, más arriesgada, más rápida de implementar, etc.

<!--more-->

## **Procesar mensajes **

Elegimos la tarea 2 y empezamos preguntándonos: ¿cómo queremos que sea el código para procesar los tweets? ¿Cuál es el código más sencillo que podemos escribir. Un ciclo de TDD siempre comienza escribiendo una prueba que falla, por lo que escribimos las respuestas de estas preguntas en una prueba que defina qué es el procesado de mensajes, cómo queremos hacerlo y qué resultado queremos obtener. Esta prueba nos permite centrar el foco de lo que implementaremos a continuación.

<pre><code class="language-python">class TestFactoriaTweets(unittest.TestCase):
	def testProcesaTweets_ConUnTweetsObtengoListaConUnElemento(self):
		tweetDePrueba = [{}]
		factoria = FactoriaTweets()
		listaDeTweets = factoria.procesaTweets(tweetDePrueba)
		self.assertEquals(1, len(listaDeTweets))</code></pre>

Con esta prueba hemos establecido que, el mecanismo para procesar los tweets es el método procesaTweets de la clase FactoriaTweets y que recibe como parámetro una lista de tweets traídos de Twitter y reduce. Después de ejecutar la prueba y comprobar que falla, vamos a implementar la FactoriaTweet y el método procesaTweets más sencillos posible.

<pre><code class="language-python">class TweetInfo:
	pass
class FactoriaTweets:
	def procesaTweets(self, mensajes):
		resultado = list()
		for m in mensajes:
			resultado.append(TweetInfo())
		return resultado</code></pre>

TweetInfo es la clase dónde almacenaremos la información relevante de cada tweet. Ahora es una clase vacía porque aún hay ninguna prueba que obligue a implementarla. Antes de continuar vamos a actualizar el diario de diseño. A partir de esa prueba descubrimos más tareas que anotamos en el diario de diseño.

<table border="1" cellspacing="0" cellpadding="0">
  <tr>
    <td valign="top" width="576">
      <b>Cuadro 2. Diario de diseño.</b>
    </td>
  </tr>
  
  <tr>
    <td valign="top" width="576">
      1) Conectarse a Internet y obtener los mensajes que contengan un tag concreto.<br /> 2) Procesar los tweets para obtener el nombre y dirección Twitter del autor, la fecha y el contenido del tweet.</p> 
      
      <ul>
        <ul>
          2.1) Definir el contenido de tweetDePrueba
        </ul>
      </ul>
      
      <ul>
        2.2) Lo elementos de la lista resultante deben tener el nombre y dirección Twitter del autor, la fecha y el contenido del tweet.
      </ul>
      
      <p>
        3) Guardar la información anterior en un nuevo fichero<br /> 4) Crear una interfaz de usuario por línea de comandos.</td> </tr> </tbody> </table> 
        
        <p>
          Vamos a continuar con estas dos nuevas tareas. Necesitamos la información de entrada (tweetDePrueba) para poder ejecutar la prueba. Twitter nos responde una cadena de texto en formato JSon, por tanto, después de procesar dicha cadena, lo que tendremos es una lista de dicts. Cada dict representará un tweet y las claves de dicho dict serán los campos de un tweet como la persona que lo escribió, el contenido, la fecha, etc. Vamos a plasmar lo anterior en una nueva prueba.
        </p>
        
        <pre><code class="language-python">def testProcesaTweets_ConUnTweetsObtengoUnTwwetInfo(self):
		rawTweet = u"""[{"created_at":"FechaCreacion",
						"from_user":"DireccionTwitter",
						"from_user_name":"NombreUsuario",
						"text":"Texto"}]"""
		tweetDePrueba = json.loads(rawTweet)
		factoria = FactoriaTweets()
		listaDeTweets = factoria.procesaTweets(tweetDePrueba)
		# asserts</code></pre>
        
        <p>
          En este caso, para simular un mensaje podría haber puesto un <i>dict</i> con los pares clave-valor que devuelve JSon, pero me ha sido más cómodo modificar la cadena devuelta por Twitter y llamar al procesador de JSon de Python.
        </p>
        
        <p>
          Esta prueba no está completa porque no tenemos nada que comprobar con la información de entrada, por lo que vamos a implementar el paso 2.3. Para ello vamos a definir, con una prueba, la clase que contendrá la información que queremos de cada tweet.
        </p>
        
        <pre><code class="language-python">class TestTweetInfo(unittest.TestCase):
	def testCreateTweetInfoAndStoreInformation(self):
		ti = TweetInfo("DireccionTwitter", "NombreUsuario", "Texto", "FechaCreacion")
		self.assertEquals(ti.direccionOrigen, "DireccionTwitter")
		self.assertEquals(ti.usuarioOrigen, "NombreUsuario")
		self.assertEquals(ti.contenido, "Texto")
		self.assertEquals(ti.fechaCreacion, "FechaCreacion")</code></pre>
        
        <p>
          Puede parecer un desperdicio de tiempo escribir una prueba para verificar una clase tan sencilla como TweetInfo, y es cierto. Sin embargo no hay que olvidar que en TDD escribimos pruebas para implementar código, por tanto la prueba anterior tiene la misión de empujarnos implementar la clase TweetInfo y también a valorar cómo pasarle la información que almacena y cómo recuperarla.<br /> Vamos a incorporar nuestra reciente clase TweetInfo a la prueba del código 3. El resultado se muestra a continuación.
        </p>
        
        <pre><code class="language-python">def testProcesaTweets_ConUnTweetsObtengoListaConUnElemento(self):
		rawTweet = u"""[{"created_at":"FechaCreacion",
						"from_user":"DireccionTwitter",
						"from_user_name":"NombreUsuario",
						"text":"Texto"}]"""
		tweetDePrueba = json.loads(rawTweet)
		factoria = FactoriaTweets()
		listaDeTweets = factoria.procesaTweets(tweetDePrueba)
		self.assertEquals(1, len(listaDeTweets))
	def testProcesaTweets_ConUnTweetsObtengoUnTweetInfo(self):
		rawTweet = u"""[{"created_at":"FechaCreacion",
						"from_user":"DireccionTwitter",
						"from_user_name":"NombreUsuario",
						"text":"Texto"}]"""
		tweetDePrueba = json.loads(rawTweet)
		factoria = FactoriaTweets()
		listaDeTweets = factoria.procesaTweets(tweetDePrueba)
		tweetInfo = listaDeTweets[0]
		self.assertEquals(tweetInfo.direccionOrigen,
						  tweetDePrueba[0]["from_user"])
		self.assertEquals(tweetInfo.usuarioOrigen,
						  tweetDePrueba[0]["from_user_name"])
		self.assertEquals(tweetInfo.contenido, tweetDePrueba[0]["text"])
		self.assertEquals(tweetInfo.fechaCreacion, tweetDePrueba[0]["created_at"])</code></pre>
        
        <p>
          Las pruebas fallan porque el código de producción no está utilizando TweetInfo. Vamos a añadirlo tal y como se muestra a continuación.
        </p>
        
        <pre><code class="language-python">class FactoriaTweets:
	def procesaTweets(self, mensajes):
		resultado = list()
		for m in mensajes:
			resultado.append(TweetInfo(m[u'from_user'], m["from_user_name"],
									   m["text"], m["created_at"]))
		return resultado</code></pre>
        
        <p>
          Verificamos las pruebas y ambas pasan. Ya podemos tachar ambas tareas en nuestro diario de diseño.
        </p>
        
        <table border="1" cellspacing="0" cellpadding="0">
          <tr>
            <td valign="top" width="576">
              <b>Cuadro 3. Diario de diseño.</b>
            </td>
          </tr>
          
          <tr>
            <td valign="top" width="576">
              1) Conectarse a Internet y obtener los mensajes que contengan un tag concreto.<span style="text-decoration:line-through;"><br /> 2) Procesar los tweets para obtener el nombre y dirección twitter del autor, la fecha y el contenido del tweet.</span><span style="text-decoration:line-through;">2.1) Definir el contenido de tweetDePrueba</span><br /> <span style="text-decoration:line-through;">2.2) Los elementos de la lista resultante deben tener el nombre y dirección twitter del autor, la fecha y el contenido del tweet. </span>3) Guardar la información anterior en un nuevo fichero.<br /> 4) Crear una interfaz de usuario por línea de comandos.
            </td>
          </tr>
        </table>
        
        <h2>
          <b>La primera refactorización<br /> </b>
        </h2>
        
        <p>
          Un ciclo de TDD no está terminado sin una refactorización tanto del código de producción como del código de pruebas.
        </p>
        
        <p>
          Cuando aplicamos TDD solemos hacer ciclos muy cortos de prueba a código y vuelta a la prueba. Con esto buscamos  la seguridad de que todos lo que implementamos funciona antes de escribir nuevo código, por también hace que estemos muy centrados en el fragmento de código que estemos trabajando y que perdamos de vista la visión global.
        </p>
        
        <p>
          En la refactorización vemos el código de manera global y en modificar el código para que sea más sencillo de entender y cambiar. TDD nos hace a escribir código de manera incremental por lo que si nuestra base no está bien diseñada ni es fácil de entender, el trabajo de añadir nuevo código se hará cada vez más lento y difícil.
        </p>
        
        <p>
          Vamos a comenzar refactorizando el código de pruebas y, en concreto, por la clase TestFactoriaTweets que contiene las pruebas de FactoriaTweets. Aunque lo hemos visto antes, vamos a mostrar todo el código de la prueba.
        </p>
        
        <pre><code class="language-python">class TestFactoriaTweets(unittest.TestCase):
	def testProcesaTweets_ConUnTweetsObtengoListaConUnElemento(self):
		rawTweet = u"""[{"created_at":"FechaCreacion",
						"from_user":"DireccionTwitter",
						"from_user_name":"NombreUsuario",
						"text":"Texto"}]"""
		tweetDePrueba = json.loads(rawTweet)
		factoria = FactoriaTweets()
		listaDeTweets = factoria.procesaTweets(tweetDePrueba)
		self.assertEquals(1, len(listaDeTweets))
	def testProcesaTweets_ConUnTweetsObtengoUnTweetInfo(self):
		rawTweet = u"""[{"created_at":"FechaCreacion",
						"from_user":"DireccionTwitter",
						"from_user_name":"NombreUsuario",
						"text":"Texto"}]"""
		tweetDePrueba = json.loads(rawTweet)
		factoria = FactoriaTweets()
		listaDeTweets = factoria.procesaTweets(tweetDePrueba)
		tweetInfo = listaDeTweets[0]
		self.assertEquals(tweetInfo.direccionOrigen,
						  tweetDePrueba[0]["from_user"])
		self.assertEquals(tweetInfo.usuarioOrigen,
						  tweetDePrueba[0]["from_user_name"])
		self.assertEquals(tweetInfo.contenido, tweetDePrueba[0]["text"])
		self.assertEquals(tweetInfo.fechaCreacion, tweetDePrueba[0]["created_at"])</code></pre>
        
        <p>
          Podemos ver varias líneas repetidas entre las dos pruebas, así que nuestra primera refactorización va a ir a evitarlas. En las herramientas XUnit, como unittest, se puede definir un método setUp que se ejecuta automáticamente andes de cada prueba, por lo que es el sitio ideal para crear el tweet de prueba.
        </p>
        
        <p>
          En la segunda prueba vemos que necesitamos varios asserts para comprobar que el mensaje coincide con el tweet de entrada. Vamos a aplicar otra refactorización y extraer estos asserts a un método auxiliar para que el objetivo de la prueba quede más claro. El resultado final se muestra a continuación.
        </p>
        
        <pre><code class="language-python">class TestFactoriaTweets(unittest.TestCase):
	def setUp(self):
		rawTweet = u"""[{"created_at":"FechaCreacion",
						"from_user":"DireccionTwitter",
						"from_user_name":"NombreUsuario",
						"text":"Texto"}]"""
		self.tweetDePrueba = json.loads(rawTweet)
		self.factoria = FactoriaTweets()
	def testProcesaTweets_ConUnTweetsObtengoListaConUnElemento(self):
		listaDeTweets = self.factoria.procesaTweets(self.tweetDePrueba)
		self.assertEquals(1, len(listaDeTweets))
	def testProcesaTweets_ConUnTweetsObtengoUnTweetInfo(self):
		listaDeTweets = self.factoria.procesaTweets(self.tweetDePrueba)
		self.assertEqualsToTweetDePrueba(listaDeTweets[0])
	def assertEqualsToTweetDePrueba(self, tweetInfo):
		self.assertEquals(tweetInfo.direccionOrigen,
						  self.tweetDePrueba[0]["from_user"])
		self.assertEquals(tweetInfo.usuarioOrigen,
						  self.tweetDePrueba[0]["from_user_name"])
		self.assertEquals(tweetInfo.contenido, self.tweetDePrueba[0]["text"])
		self.assertEquals(tweetInfo.fechaCreacion,
						  self.tweetDePrueba[0]["created_at"])</code></pre>
        
        <p>
          Pasamos ahora refactorizamos el código de producción, siempre asegurándonos de que después de cada cambio las pruebas siguen funcionando correctamente.<br /> Aunque por la brevedad del código podríamos pensar que no es necesaria una refactorización, sí que existe un mal olor en el código. Si nos fijamos, el método procesaTweets tiene dos responsabilidades distintas que son procesar toda la lista de tweets y crear un objeto TweetInfo por cada tweet. Vamos a separar ambas funcionalidades en dos métodos aparte. El código resultante se muestra a continuación.
        </p>
        
        <pre><code class="language-python">class FactoriaTweets:
	def procesaTweets(self, mensajes):
		resultado = list()
		for m in mensajes:
			resultado.append(self._creaTweetInfo(m))
		return resultado
	def _creaTweetInfo(self, tweetDict):
		return TweetInfo(tweetDict[u'from_user'], tweetDict["from_user_name"],
						 tweetDict["text"], tweetDict["created_at"])</code></pre>
        
        <p>
          En este caso, hemos creado un nuevo método pero no hemos escrito una prueba antes. Veamos el por qué. En este método no escribimos nuevo código, solo cambiamos un código que ya funciona de sitio. El nuevo método está siendo probado por las pruebas que tenemos. Además, al ser privado pedimos que nos e acceda directamente a él.
        </p>
        
        <h2>
          <strong>Pruebas cómo documentación</strong>
        </h2>
        
        <p>
          También podemos utilizar las pruebas para documentar el funcionamiento del código aunque no realicemos un ciclo TDD. Por ejemplo, ¿qué sucede si nuestra entrada no contiene ningún tweet nuestra salida será una lista vacía?. Definamos este escenario con una prueba.
        </p>
        
        <pre><code class="language-python">def testProcesaTweets_SinTweetsObtengoListaConUnElemento(self):
		listaDeTweets = self.factoria.procesaTweets([])
		self.assertEquals(0, len(listaDeTweets))</code></pre>
        
        <p>
          Al ejecutar la prueba comprobamos que el resultado es el esperado por lo que no es necesario implementar nada. Antes de añadir pruebas adicionales hemos de tener en cuenta el ost de su mantenimiento. Demasiadas pruebas puede ser contraproducentes pro dedicar un esfuerzo innecesario. Además, un código con demasiadas pruebas puede ofrecer resistencia al cambio por la gran cantidad de pruebas afectadas
        </p>
        
        <h2>
          <b>Conclusiones</b>
        </h2>
        
        <p>
          Hemos visto algunos aspectos muy interesantes sobre cómo aplicar TDD como no preocuparnos de algo hasta que no lo necesitamos. Vamos a darles un último repaso ya que seguiremos aplicándolos en las próximas entregas.
        </p>
        
        <p>
          Hemos intentado escribir sólo el código que necesitamos. Por ejemplo, en la primera prueba no hemos indicado ni la información del tweet ni la información de salida, porque no era necesario aún. Esto nos ha permitido empezar a codificar más rápido y centrarnos solo en cómo procesar los tweets recibidos. También hemos refactorizado para evitar duplicación de código y para mejorar la legibilidad escondiendo detalles detrás de métodos. Por último, hemos hecho ciclos rápidos con poco código y pruebas pequeñas para tener la tranquilidad de que todo lo anterior funciona antes de empezar a programar algo nuevo.
        </p>
        
        <p>
          Y aquí terminamos esta primera entrega. En la próxima, en una o dos semanas, implementaremos una nueva tarea del diario de diseño aplicando TDD. Continuaremos aplicando todo lo que hemos aprendido en esta entrega y, además presentaremos los dobles de prueba (también llamados test doubles).
        </p>
        
        <p>
          Hasta pronto.
        </p>
        
        <div style="background-color:#eee;padding:.5em 1em .15em;margin-bottom:1em;">
          Este artículo es fruto de la colaboración entre Javier Gutiérrez y Juan Luis Cano, que aportó sugerencias y correcciones al original.</p>
        </div>