---
title: Joyitas en la stdlib: pathlib
date: 2016-05-18T22:06:30+00:00
author: Kiko Correoso
slug: joyitas-en-la-stdlib-pathlib
tags: directorios, ficheros, path, pathlib, rutas, stdlib

<div>
  <div>
  </div>
  
  <div>
    <div>
      <p>
        El otro día estuvimos hablando de la <a href="http://pybonacci.org/2016/05/08/joyitas-en-la-stdlib-collections/">biblioteca <code>collections</code></a>, una joya dentro de la librería estándar. Hoy vamos a hablar de una nueva biblioteca que se incluyó en la versión 3.4 de CPython llamada <a href="https://docs.python.org/3/library/pathlib.html"><code>pathlib</code></a>.
      </p>
      
      <p>
        <strong>Solo python 3, actualízate!!!</strong>
      </p>
      
      <p>
        Esta biblioteca nos da la posibilidad de usar clases para trabajar con las rutas del sistema de ficheros con una serie de métodos muy interesantes.
      </p>
      
      <h2 id="Algunas-utilidades-para-configurar-el-problema">
        Algunas utilidades para configurar el problema<a class="anchor-link" href="#Algunas-utilidades-para-configurar-el-problema">¶</a>
      </h2>
      
      <p>
        Vamos a crear un par de funciones que nos permiten crear y borrar un directorio de pruebas para poder reproducir el ejemplo de forma sencilla:
      </p>
    </div>
  </div>
</div>

<div>
  <div>
    <div>
      <div>
        <div class=" highlight hl-ipython3">
          <pre><span class="kn">import</span> <span class="nn">os</span>
<span class="kn">import</span> <span class="nn">glob</span>
<span class="kn">import</span> <span class="nn">shutil</span>
<span class="kn">from</span> <span class="nn">random</span> <span class="k">import</span> <span class="n">randint</span><span class="p">,</span> <span class="n">choice</span><span class="p">,</span> <span class="n">seed</span>
<span class="kn">from</span> <span class="nn">string</span> <span class="k">import</span> <span class="n">ascii_letters</span>

<span class="c1"># función que nos crea un directorio de prueba en</span>
<span class="c1"># el mismo directorio del notebook</span>
<span class="k">def</span> <span class="nf">crea_directorio</span><span class="p">():</span>
    <span class="n">seed</span><span class="p">(</span><span class="mi">1</span><span class="p">)</span>
    <span class="n">base</span> <span class="o">=</span> <span class="n">os</span><span class="o">.</span><span class="n">path</span><span class="o">.</span><span class="n">join</span><span class="p">(</span><span class="n">os</span><span class="o">.</span><span class="n">path</span><span class="o">.</span><span class="n">curdir</span><span class="p">,</span>
                        <span class="s1">'pybonacci_probando_pathlib'</span><span class="p">)</span>
    <span class="n">os</span><span class="o">.</span><span class="n">makedirs</span><span class="p">(</span><span class="n">base</span><span class="p">,</span> <span class="n">exist_ok</span> <span class="o">=</span> <span class="kc">True</span><span class="p">)</span>

    <span class="k">for</span> <span class="n">i</span> <span class="ow">in</span> <span class="nb">range</span><span class="p">(</span><span class="mi"></span><span class="p">,</span> <span class="n">randint</span><span class="p">(</span><span class="mi">3</span><span class="p">,</span> <span class="mi">5</span><span class="p">)):</span>
        <span class="n">folder</span> <span class="o">=</span> <span class="s1">''</span><span class="o">.</span><span class="n">join</span><span class="p">([</span><span class="n">choice</span><span class="p">(</span><span class="n">ascii_letters</span><span class="p">)</span> <span class="k">for</span> <span class="n">_</span> <span class="ow">in</span> <span class="nb">range</span><span class="p">(</span><span class="mi">4</span><span class="p">)])</span>
        <span class="n">path</span> <span class="o">=</span> <span class="n">os</span><span class="o">.</span><span class="n">path</span><span class="o">.</span><span class="n">join</span><span class="p">(</span><span class="n">base</span><span class="p">,</span> <span class="n">folder</span><span class="p">)</span>
        <span class="n">os</span><span class="o">.</span><span class="n">makedirs</span><span class="p">(</span><span class="n">path</span><span class="p">,</span> <span class="n">exist_ok</span> <span class="o">=</span> <span class="kc">True</span><span class="p">)</span>
        <span class="k">for</span> <span class="n">j</span> <span class="ow">in</span> <span class="nb">range</span><span class="p">(</span><span class="mi"></span><span class="p">,</span> <span class="n">randint</span><span class="p">(</span><span class="mi">2</span><span class="p">,</span> <span class="mi">5</span><span class="p">)):</span>
            <span class="n">ext</span> <span class="o">=</span> <span class="n">choice</span><span class="p">([</span><span class="s1">'.txt'</span><span class="p">,</span> <span class="s1">'.py'</span><span class="p">,</span> <span class="s1">'.html'</span><span class="p">])</span>
            <span class="n">name</span> <span class="o">=</span> <span class="s1">''</span><span class="o">.</span><span class="n">join</span><span class="p">([</span><span class="n">choice</span><span class="p">(</span><span class="n">ascii_letters</span><span class="p">)</span> <span class="k">for</span> <span class="n">_</span> <span class="ow">in</span> <span class="nb">range</span><span class="p">(</span><span class="n">randint</span><span class="p">(</span><span class="mi">5</span><span class="p">,</span> <span class="mi">10</span><span class="p">))])</span>
            <span class="n">filename</span> <span class="o">=</span> <span class="n">name</span> <span class="o">+</span> <span class="n">ext</span>
            <span class="n">path2</span> <span class="o">=</span> <span class="n">os</span><span class="o">.</span><span class="n">path</span><span class="o">.</span><span class="n">join</span><span class="p">(</span><span class="n">path</span><span class="p">,</span> <span class="n">filename</span><span class="p">)</span>
            <span class="nb">open</span><span class="p">(</span><span class="n">path2</span><span class="p">,</span> <span class="s1">'w'</span><span class="p">)</span><span class="o">.</span><span class="n">close</span><span class="p">()</span>

<span class="c1"># Función que nos permite hacer limpieza            </span>
<span class="k">def</span> <span class="nf">borra_directorio</span><span class="p">():</span>
    <span class="n">base</span> <span class="o">=</span> <span class="n">os</span><span class="o">.</span><span class="n">path</span><span class="o">.</span><span class="n">join</span><span class="p">(</span><span class="n">os</span><span class="o">.</span><span class="n">path</span><span class="o">.</span><span class="n">curdir</span><span class="p">,</span>
                        <span class="s1">'pybonacci_probando_pathlib'</span><span class="p">)</span>
    <span class="n">shutil</span><span class="o">.</span><span class="n">rmtree</span><span class="p">(</span><span class="n">base</span> <span class="o">+</span> <span class="n">os</span><span class="o">.</span><span class="n">path</span><span class="o">.</span><span class="n">sep</span><span class="p">)</span>
</pre>
        </div>
      </div>
    </div>
  </div>
</div>

<div>
  <div>
  </div>
  
  <div>
    <div>
      <p>
        Si ahora ejecutamos la función <code>crea_directorio</code>:
      </p>
    </div>
  </div>
</div>

<div>
  <div>
    <div>
      <div>
        <div class=" highlight hl-ipython3">
          <pre><span class="n">crea_directorio</span><span class="p">()</span>
</pre>
        </div>
      </div>
    </div>
  </div>
</div>

<div>
  <div>
  </div>
  
  <div>
    <div>
      <p>
        Nos debería quedar una estructura parecida a lo siguiente:
      </p>
      
          :::[]
    pybonacci_probando_pathlib/
    ├── KZWe
    │   ├── CrUZoLgubb.txt
    │   ├── IayRnBUbHo.txt
    │   ├── WCEPyYng.txt
    │   └── yBMWX.py
    ├── WCFJ
    │   ├── GBGQmtsLFG.html
    │   ├── PglOUshVv.py
    │   └── RoWDsb.py
    └── zLcE
        ├── AQlxJSXR.html
        ├── fCQGgXk.html
        └── xFUbEctT.html
    
    
    
      
      <h2 id="Ejemplo-usando-lo-disponible-hasta-hace-poco">
        Ejemplo usando lo disponible hasta hace poco<a class="anchor-link" href="#Ejemplo-usando-lo-disponible-hasta-hace-poco">¶</a>
      </h2>
      
      <p>
        Pensemos en un problema que consiste en identificar todos los ficheros <em>.py</em> disponibles en determinada ruta y dejarlos en una nueva carpeta, que llamaremos <em>python</em>, todos juntos eliminándolos de la carpeta original en la que se encuentren.
      </p>
      
      <p>
        De la forma antigua esto podría ser así:
      </p>
    </div>
  </div>
</div>

<div>
  <div>
    <div>
      <div>
        <div class=" highlight hl-ipython3">
          <pre><span class="c1"># Suponemos que ya has creado los directorios y ficheros</span>
<span class="c1"># de prueba usando crea_directorio()</span>

<span class="c1"># recolectamos todos los ficheros *.py con sus rutas</span>
<span class="n">base</span> <span class="o">=</span> <span class="n">os</span><span class="o">.</span><span class="n">path</span><span class="o">.</span><span class="n">join</span><span class="p">(</span><span class="n">os</span><span class="o">.</span><span class="n">path</span><span class="o">.</span><span class="n">curdir</span><span class="p">,</span>
                    <span class="s1">'pybonacci_probando_pathlib'</span><span class="p">)</span>
<span class="n">ficheros_py</span> <span class="o">=</span> <span class="n">glob</span><span class="o">.</span><span class="n">glob</span><span class="p">(</span><span class="n">os</span><span class="o">.</span><span class="n">path</span><span class="o">.</span><span class="n">join</span><span class="p">(</span><span class="n">base</span><span class="p">,</span> <span class="s1">'**'</span><span class="p">,</span> <span class="s1">'*.py'</span><span class="p">))</span>

<span class="c1"># creamos la carpeta 'python' </span>
<span class="c1"># dentro de 'pybonacci_probando_pathlib'</span>
<span class="n">os</span><span class="o">.</span><span class="n">makedirs</span><span class="p">(</span><span class="n">os</span><span class="o">.</span><span class="n">path</span><span class="o">.</span><span class="n">join</span><span class="p">(</span><span class="n">base</span><span class="p">,</span> <span class="s1">'python'</span><span class="p">),</span> <span class="n">exist_ok</span> <span class="o">=</span> <span class="kc">True</span><span class="p">)</span>

<span class="c1"># y movemos los ficheros a la nueva carpeta 'python'</span>
<span class="k">for</span> <span class="n">f</span> <span class="ow">in</span> <span class="n">ficheros_py</span><span class="p">:</span>
    <span class="n">fich</span> <span class="o">=</span> <span class="n">f</span><span class="o">.</span><span class="n">split</span><span class="p">(</span><span class="n">os</span><span class="o">.</span><span class="n">path</span><span class="o">.</span><span class="n">sep</span><span class="p">)[</span><span class="o">-</span><span class="mi">1</span><span class="p">]</span>
    <span class="n">shutil</span><span class="o">.</span><span class="n">move</span><span class="p">(</span><span class="n">f</span><span class="p">,</span> <span class="n">os</span><span class="o">.</span><span class="n">path</span><span class="o">.</span><span class="n">join</span><span class="p">(</span><span class="n">base</span><span class="p">,</span> <span class="s1">'python'</span><span class="p">))</span>
</pre>
        </div>
      </div>
    </div>
  </div>
</div>

<div>
  <div>
  </div>
  
  <div>
    <div>
      <p>
        Nuestra nueva estructura de ficheros debería ser la siguiente:
      </p>
      
          :::[]
    pybonacci_probando_pathlib/
    ├── KZWe
    │   ├── CrUZoLgubb.txt
    │   ├── IayRnBUbHo.txt
    │   └── WCEPyYng.txt
    ├── python
    │   ├── PglOUshVv.py
    │   ├── RoWDsb.py
    │   └── yBMWX.py
    ├── WCFJ
    │   └── GBGQmtsLFG.html
    └── zLcE
        ├── AQlxJSXR.html
        ├── fCQGgXk.html
        └── xFUbEctT.html
    
    
      
      <p>
        En el anterior ejemplo hemos tenido que usar las bibliotecas <code>glob</code>, <code>os</code> y <code>shutil</code> para poder realizar una operación relativamente sencilla. Esto no es del todo deseable porque he de conocer tres librerías diferentes y mi cabeza no da para tanto.
      </p>
      
      <h2 id="Limpieza">
        Limpieza<a class="anchor-link" href="#Limpieza">¶</a>
      </h2>
      
      <p>
        Me cargo la carpeta <em>pybonacci_probando_pathlib</em> para hacer un poco de limpieza:
      </p>
    </div>
  </div>
</div>

<div>
  <div>
    <div>
      <div>
        <div class=" highlight hl-ipython3">
          <pre><span class="n">borra_directorio</span><span class="p">()</span>
</pre>
        </div>
      </div>
    </div>
  </div>
</div>

<div>
  <div>
  </div>
  
  <div>
    <div>
      <p>
        Y vuelvo a crear la estructura de ficheros inicial:
      </p>
    </div>
  </div>
</div>

<div>
  <div>
    <div>
      <div>
        <div class=" highlight hl-ipython3">
          <pre><span class="n">crea_directorio</span><span class="p">()</span>
</pre>
        </div>
      </div>
    </div>
  </div>
</div>

<div>
  <div>
  </div>
  
  <div>
    <div>
      <p>
        Después de la limpieza vamos a afrontar el problema usando <code>pathlib</code>.
      </p>
      
      <h2 id="El-mismo-ejemplo-con-pathlib">
        El mismo ejemplo con <code>pathlib</code><a class="anchor-link" href="#El-mismo-ejemplo-con-pathlib">¶</a>
      </h2>
      
      <p>
        Primero importamos la librería y, como bonus, creamos una función que hace lo mismo que la función <code>borra_directorio</code> pero usando <code>pathlib</code>, que llamaremos <code>borra_directorio_pathlib</code>:
      </p>
    </div>
  </div>
</div>

<div>
  <div>
    <div>
      <div>
        <div class=" highlight hl-ipython3">
          <pre><span class="kn">from</span> <span class="nn">pathlib</span> <span class="k">import</span> <span class="n">Path</span>

<span class="k">def</span> <span class="nf">borra_directorio_pathlib</span><span class="p">(</span><span class="n">path</span> <span class="o">=</span> <span class="kc">None</span><span class="p">):</span>
    <span class="k">if</span> <span class="n">path</span> <span class="ow">is</span> <span class="kc">None</span><span class="p">:</span>
        <span class="n">p</span> <span class="o">=</span> <span class="n">Path</span><span class="p">(</span><span class="s1">'.'</span><span class="p">,</span> <span class="s1">'pybonacci_probando_pathlib'</span><span class="p">)</span>
    <span class="k">else</span><span class="p">:</span>
        <span class="n">p</span> <span class="o">=</span> <span class="n">path</span>
    <span class="k">for</span> <span class="n">i</span> <span class="ow">in</span> <span class="n">p</span><span class="o">.</span><span class="n">iterdir</span><span class="p">():</span>
        <span class="k">if</span> <span class="n">i</span><span class="o">.</span><span class="n">is_dir</span><span class="p">():</span>
            <span class="n">borra_directorio_pathlib</span><span class="p">(</span><span class="n">i</span><span class="p">)</span>
        <span class="k">else</span><span class="p">:</span>
            <span class="n">i</span><span class="o">.</span><span class="n">unlink</span><span class="p">()</span>
    <span class="n">p</span><span class="o">.</span><span class="n">rmdir</span><span class="p">()</span>
</pre>
        </div>
      </div>
    </div>
  </div>
</div>

<div>
  <div>
  </div>
  
  <div>
    <div>
      <p>
        La anterior función con <code>shutil</code> es un poco más sencilla que con <code>pathlib</code>. Esto es lo único que hecho de menos en <code>pathlib</code>, algunas utilidades de <code>shutil</code> que vendrían muy bien de serie. Algo negativo tenía que tener.
      </p>
      
      <p>
        En la anterior función, <code>borra_directorio_pathlib</code>, podemos ver ya algunas cositas de <code>pathlib</code>.
      </p>
      
      <p>
        <code>p = Path('.', 'pybonacci_probando_pathlib')</code> nos crea una ruta que ahora es un objeto en lugar de una cadena. Dentro del bucle usamos el método <a href="https://docs.python.org/3/library/pathlib.html#pathlib.Path.iterdir"><code>iterdir</code></a> que nos permite iterar sobre los directorios de la ruta definida en el objeto <code>p</code>. el iterador nos devuelve nuevos objetos que disponen de métodos como <a href="https://docs.python.org/3/library/pathlib.html#pathlib.Path.is_dir"><code>is_dir</code></a>, que nos permite saber si una ruta se refiere a un directorio, o <a href="https://docs.python.org/3/library/pathlib.html#pathlib.Path.unlink"><code>unlink</code></a>, que nos permite eliminar el fichero o enlace. Por último, una vez que no tenemos ficheros dentro del directorio definido en <code>p</code> podemos usar el método <a href="https://docs.python.org/3/library/pathlib.html#pathlib.Path.rmdir"><code>rmdir</code></a> para eliminar la carpeta.
      </p>
      
      <p>
        Ahora veamos cómo realizar lo mismo que antes usando <code>pathlib</code>, es decir, mover los ficheros <em>.py</em> a la carpeta <em>python</em> que hemos de crear.
      </p>
    </div>
  </div>
</div>

<div>
  <div>
    <div>
      <div>
        <div class=" highlight hl-ipython3">
          <pre><span class="c1"># recolectamos todos los ficheros *.py con sus rutas</span>
<span class="n">p</span> <span class="o">=</span> <span class="n">Path</span><span class="p">(</span><span class="s1">'.'</span><span class="p">,</span> <span class="s1">'pybonacci_probando_pathlib'</span><span class="p">)</span>
<span class="n">ficheros_py</span> <span class="o">=</span> <span class="n">p</span><span class="o">.</span><span class="n">glob</span><span class="p">(</span><span class="s1">'**/*.py'</span><span class="p">)</span>

<span class="c1"># creamos la carpeta 'python' dentro de 'pybonacci_probando_pathlib'</span>
<span class="p">(</span><span class="n">p</span> <span class="o">/</span> <span class="s1">'python'</span><span class="p">)</span><span class="o">.</span><span class="n">mkdir</span><span class="p">(</span><span class="n">mode</span> <span class="o">=</span> <span class="mo">0o777</span><span class="p">,</span> <span class="n">exist_ok</span> <span class="o">=</span> <span class="kc">True</span><span class="p">)</span>

<span class="c1"># y copiamos los ficheros a la nueva carpeta 'python'</span>
<span class="k">for</span> <span class="n">f</span> <span class="ow">in</span> <span class="n">ficheros_py</span><span class="p">:</span>
    <span class="n">target</span> <span class="o">=</span> <span class="n">p</span> <span class="o">/</span> <span class="s1">'python'</span> <span class="o">/</span> <span class="n">f</span><span class="o">.</span><span class="n">name</span>
    <span class="n">f</span><span class="o">.</span><span class="n">rename</span><span class="p">(</span><span class="n">target</span><span class="p">)</span>
</pre>
        </div>
      </div>
    </div>
  </div>
</div>

<div>
  <div>
  </div>
  
  <div>
    <div>
      <p>
        Nuevamente, nuestra estructura de ficheros debería ser la misma que antes:
      </p>
      
          :::[]
    pybonacci_probando_pathlib/
    ├── KZWe
    │   ├── CrUZoLgubb.txt
    │   ├── IayRnBUbHo.txt
    │   └── WCEPyYng.txt
    ├── python
    │   ├── PglOUshVv.py
    │   ├── RoWDsb.py
    │   └── yBMWX.py
    ├── WCFJ
    │   └── GBGQmtsLFG.html
    └── zLcE
        ├── AQlxJSXR.html
        ├── fCQGgXk.html
        └── xFUbEctT.html
    
    
      
      <p>
        Repasemos el código anterior:<br /> Hemos creado un objeto ruta <code>p</code> tal como habíamos visto antes en la función <code>borra_directorio_pathlib</code>. Este objeto ahora dispone de un método <a href="https://docs.python.org/3/library/pathlib.html#pathlib.Path.glob"><code>glob</code></a> que nos devuelve un iterador con lo que le pidamos, en este caso, todos los ficheros con extensión <em>.py</em>. En la línea <code>(p / 'python').mkdir(mode = 0o777, exist_ok = True)</code> podemos ver el uso de <code>/</code> como operador para instancias de <code>Path</code>. El primer paréntesis nos devuelve una nueva instancia de <code>Path</code> que dispone del método <a href="https://docs.python.org/3/library/pathlib.html#pathlib.Path.mkdir"><code>mkdir</code></a> que hace lo que todos esperáis. Como <code>ficheros_py</code> era un iterador podemos usarlo en el bucle obteniendo nuevas instancias de <code>Path</code> con las rutas de los ficheros python que queremos mover. en la línea donde se define <code>target</code> hacemos uso del atributo <a href="https://docs.python.org/3/library/pathlib.html#pathlib.PurePath.name"><code>name</code></a>,que nos devuelve la última parte de la ruta. Por último, el fichero con extensión <em>.py</em> definido en el <code>Path</code> <code>f</code> lo renombramos a una nueva ruta, definida en <code>target</code>.
      </p>
      
      <p>
        Y todo esto usando una única librería!!!
      </p>
      
      <p>
        Echadle un ojo a la <a href="https://docs.python.org/3/library/pathlib.html">documentación oficial</a> para descubrir otras cositas interesantes.
      </p>
      
      <p>
        Si además de usar una única librería usamos parte de la funcionalidad de <code>shutil</code> tenemos una pareja muy potente, <code>pathlib</code> + <code>shutil</code>.
      </p>
    </div>
  </div>
</div>

<div>
  <div>
  </div>
  
  <div>
    <div>
      <h2 id="Limpieza-II">
        Limpieza II<a class="anchor-link" href="#Limpieza-II">¶</a>
      </h2>
      
      <p>
        Y para terminar, limpiamos nuestra estructura de ficheros pero usando ahora la función <code>borra_directorio_pathlib</code> que habíamos creado pero no usado aún:
      </p>
    </div>
  </div>
</div>

<div>
  <div>
    <div>
      <div>
        <div class=" highlight hl-ipython3">
          <pre><span class="n">borra_directorio_pathlib</span><span class="p">()</span></pre>
          
          <h2>
            <span class="p">Notas</span>
          </h2>
          
          <p>
            Ya hay un nuevo <a href="https://www.python.org/dev/peps/pep-0519/">PEP relacionado y aceptado</a>.
          </p>
        </div>
      </div>
    </div>
  </div>
</div>

<div>
  <div>
    <div>
      <p>
        Enjoy!!
      </p>
    </div>
  </div>
</div>