---
title: Cómo acelerar tu código Python con numba
date: 2015-03-13T16:45:25+00:00
author: Juan Luis Cano
slug: como-acelerar-tu-codigo-python-con-numba
tags: conda, numba, python, python 3, rendimiento

<div>
  <div>
  </div>
  
  <div>
    <div>
      <h2 id="Introducci&#243;n">
        Introducci&#243;n<a class="anchor-link" href="#Introducci&#243;n">&#182;</a>
      </h2>
      
      <p>
        En este artículo vamos a hacer un repaso exhaustivo de <strong>cómo acelerar sustancialmente tu código Python usando numba</strong>. Ya hablamos sobre <a href="http://pybonacci.org/2012/08/21/probando-numba-compilador-para-python-basado-en-llvm/">la primera versión de numba</a> en el blog, allá por 2012, pero ha habido importantes cambios desde entonces y la herramienta ha cambiado muchísimo. Recientemente Continuum publicó numba 0.17 con una <a href="http://numba.pydata.org/numba-doc/0.17.0/index.html">nueva documentación</a> mucho más fácil de seguir, pero aun así no siempre queda claro cuál es el camino para hacer que funcione, como quedó patente con el <a href="http://pybonacci.org/2015/03/09/c-elemental-querido-cython/">artículo sobre Cython</a> de Kiko. Por ello, en este artículo voy a aclarar qué puede y qué no puede hacer numba, cómo sacarle partido y voy a detallar un par de ejemplos exitosos que he producido en los últimos meses.
      </p>
      
      <p>
      </p>
      
      <p>
        <!--more-->
      </p>
      
      <p>
        Hablando de las nuevas versiones de numba, en su web podéis ver una <a href="http://numba.pydata.org/numba-benchmark/">evolución temporal del rendimiento</a> de algunas tareas que utiliza <a href="http://spacetelescope.github.io/asv/">asv</a> para la visualización.
      </p>
    </div>
  </div>
</div>

<div>
  <div>
  </div>
  
  <div>
    <div>
      <h2 id="Entendiendo-numba:-el-modo-nopython">
        Entendiendo numba: el modo <em>nopython</em><a class="anchor-link" href="-el-modo-nopython">&#182;</a>
      </h2>
      
      <p>
        Como podemos leer en la documentación, <a href="http://numba.pydata.org/numba-doc/0.17.0/user/jit.html#nopython">numba tiene dos modos de funcionamiento básicos</a>: el modo <em>object</em> y el modo <em>nopython</em>.
      </p>
      
      <ul>
        <li>
          El modo <em>object</em> genera código que gestiona todas las variables como objetos de Python y utiliza la API C de Python para operar con ellas. En general en este modo <strong>no habrá ganancias de rendimiento</strong> (e incluso puede ir más lento), con lo cual mi recomendación personal es directamente no utilizarlo. Hay casos en los que numba puede detectar los bucles y optimizarlos individualmente (<em>loop-jitting</em>), pero no le voy a prestar mucha atención a esto.
        </li>
        <li>
          El modo <em>nopython</em> <strong>genera código independiente de la API C de Python</strong>. Esto tiene la desventaja de que no podemos usar todas las características del lenguaje, <strong>pero tiene un efecto significativo en el rendimiento</strong>. Otra de las restricciones es que <strong>no se puede reservar memoria para objetos nuevos</strong>.
        </li>
      </ul>
      
      <p>
        Por defecto numba usa el modo <em>nopython</em> siempre que puede, y si no pasa a modo <em>object</em>. Nosotros vamos a <strong>forzar el modo nopython</strong> (o «modo estricto» como me gusta llamarlo) porque es la única forma de aprovechar el potencial de numba.
      </p>
    </div>
  </div>
</div>

<div>
  <div>
  </div>
  
  <div>
    <div>
      <h2 id="&#193;mbito-de-aplicaci&#243;n">
        &#193;mbito de aplicaci&#243;n<a class="anchor-link" href="#&#193;mbito-de-aplicaci&#243;n">&#182;</a>
      </h2>
      
      <p>
        El problema del modo <em>nopython</em> es que los mensajes de error son totalmente inservibles en la mayoría de los casos, así que antes de lanzarnos a compilar funciones con numba conviene hacer un repaso de qué no podemos hacer para anticipar la mejor forma de programar nuestro código. Podéis consultar en la documentación <a href="http://numba.pydata.org/numba-doc/0.17.0/reference/pysupported.html">el subconjunto de Python soportado por numba</a> en modo <em>nopython</em>, y ya os aviso que, al menos de momento, no tenemos <a href="https://github.com/numba/numba/issues/504"><em>list comprehensions</em></a>, <a href="https://github.com/numba/numba/issues/984">generadores</a> ni algunas cosas más. Permitidme que resalte una frase sacada de la página principal de numba:
      </p>
      
      <blockquote>
        <p>
          "<em>With a few annotations, <strong>array-oriented and math-heavy Python code</strong> can be just-in-time compiled to native machine instructions, similar in performance to C, C++ and Fortran</em>". [Énfasis mío]
        </p>
      </blockquote>
      
      <p>
        Siento decepcionar a la audiencia pero <em>numba no acelerará todo el código Python</em> que le echemos: está enfocado a operaciones matemáticas con arrays. Aclarado este punto, vamos a ponernos manos a la obra con un ejemplo aplicado 🙂
      </p>
    </div>
  </div>
</div>

<div>
  <div>
  </div>
  
  <div>
    <div>
      <h2 id="Antes-de-empezar:-instalaci&#243;n">
        Antes de empezar: instalaci&#243;n<a class="anchor-link" href="-instalaci&#243;n">&#182;</a>
      </h2>
      
      <p>
        Puedes instalar numba en Windows, OS X y Linux con <a href="http://conda.io/">conda</a> usando este comando:<br /> <code>conda install numba</code><br /> conda se ocupará de instalar una versión correcta de LLVM, así que no tendrás que compilarla tú mismo. <em>Y ya está</em>.<br /> Ahora viene una opinión personal pero que considero importante: si eres usuario de paquetes científicos y aún no estás utilizando conda (o Anaconda) para gestionarlos, <strong>estás en la edad de piedra</strong>. Me declaro fanboy absoluto de Continuum Analytics por crear una herramienta de código abierto (<a href="http://github.com/conda/conda">conda está en GitHub</a>) que soluciona <em>por fin y de una vez por todas</em> los problemas y frustración que hemos tenido como comunidad <a href="https://twitter.com/fperez_org/status/569896953875722240">desde hace 15 años</a> y que Guido y otros se negaron a atajar. Yo llevo en esto solo desde 2011 pero aún recuerdo lo que es intentar compilar SciPy en Windows. Hazte un favor e <a href="http://conda.pydata.org/miniconda.html">instala Miniconda</a>.
      </p>
    </div>
  </div>
</div>

<div>
  <div>
  </div>
  
  <div>
    <div>
      <h2 id="Acelerando-una-funci&#243;n-con-numba">
        Acelerando una funci&#243;n con numba<a class="anchor-link" href="#Acelerando-una-funci&#243;n-con-numba">&#182;</a>
      </h2>
      
      <p>
        Voy a tomar directamente el ejemplo que usó Kiko para su artículo sobre Cython y vamos a ver cómo podemos utilizar numba (y un poco de astucia) para acelerar esta función:
      </p>
      
      <blockquote>
        <p>
          "Por ejemplo, imaginemos que tenemos que detectar valores mínimos locales dentro de una malla. Los valores mínimos deberán ser simplemente valores más bajos que los que haya en los 8 nodos de su entorno inmediato. En el siguiente gráfico, el nodo en verde será un nodo con un mínimo y en su entorno son todo valores superiores:
        </p>
      </blockquote>
      
      <table>
        <tr>
          <td style="background:red">
            (2, 0)
          </td>
          
          <td style="background:red">
            (2, 1)
          </td>
          
          <td style="background:red">
            (2, 2)
          </td>
        </tr>
        
        <tr>
          <td style="background:red">
            (1, 0)
          </td>
          
          <td style="background:green">
            (1. 1)
          </td>
          
          <td style="background:red">
            (1, 2)
          </td>
        </tr>
        
        <tr>
          <td style="background:red">
            (0, 0)
          </td>
          
          <td style="background:red">
            (0, 1)
          </td>
          
          <td style="background:red">
            (0, 2)
          </td>
        </tr>
      </table>
      
      <p>
        ¡Vamos allá!
      </p>
    </div>
  </div>
</div>

<div>
  <div>
    <div>
      <div>
        <div class=" highlight hl-ipython3">
          <pre><span class="o">%</span><span class="k">install_ext</span> http://raw.github.com/jrjohansson/version_information/master/version_information.py
</pre>
        </div>
      </div>
    </div>
  </div>
  
  <div>
    <div>
      <div>
        <div>
        </div>
        
        <div>
          <pre>Installed version_information.py. To use it, type:
  %load_ext version_information
</pre>
        </div>
      </div>
    </div>
  </div>
</div>

<div>
  <div>
    <div>
      <div>
        <div class=" highlight hl-ipython3">
          <pre><span class="o">%</span><span class="k">load_ext</span> version_information
</pre>
        </div>
      </div>
    </div>
  </div>
</div>

<div>
  <div>
    <div>
      <div>
        <div class=" highlight hl-ipython3">
          <pre><span class="o">%</span><span class="k">version_information</span> numpy, numba, cython
</pre>
        </div>
      </div>
    </div>
  </div>
  
  <div>
    <div>
      <div>
        <div>
        </div>
        
        <div>
          <table>
            <tr>
              <th>
                Software
              </th>
              
              <th>
                Version
              </th>
            </tr>
            
            <tr>
              <td>
                Python
              </td>
              
              <td>
                3.4.3 64bit [GCC 4.4.7 20120313 (Red Hat 4.4.7-1)]
              </td>
            </tr>
            
            <tr>
              <td>
                IPython
              </td>
              
              <td>
                3.0.0
              </td>
            </tr>
            
            <tr>
              <td>
                OS
              </td>
              
              <td>
                Linux 3.18.6 1 ARCH x86_64 with arch
              </td>
            </tr>
            
            <tr>
              <td>
                numpy
              </td>
              
              <td>
                1.9.2
              </td>
            </tr>
            
            <tr>
              <td>
                numba
              </td>
              
              <td>
                0.17.0
              </td>
            </tr>
            
            <tr>
              <td>
                cython
              </td>
              
              <td>
                0.22
              </td>
            </tr>
            
            <tr>
              <td colspan='2'>
                Fri Mar 13 13:44:39 2015 CET
              </td>
            </tr>
          </table>
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
      Vamos a empezar por importar los paquetes necesarios e inicializar la semilla del generador de números aleatorios:</p>
    </div>
  </div>
</div>

<div>
  <div>
    <div>
      <div>
        <div class=" highlight hl-ipython3">
          <pre><span class="kn">import</span> <span class="nn">numpy</span> <span class="k">as</span> <span class="nn">np</span>
<span class="kn">import</span> <span class="nn">numba</span>

<span class="n">np</span><span class="o">.</span><span class="n">random</span><span class="o">.</span><span class="n">seed</span><span class="p">(</span><span class="mi"></span><span class="p">)</span>
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
      Creamos nuestro array de datos:</p>
    </div>
  </div>
</div>

<div>
  <div>
    <div>
      <div>
        <div class=" highlight hl-ipython3">
          <pre><span class="n">data</span> <span class="o">=</span> <span class="n">np</span><span class="o">.</span><span class="n">random</span><span class="o">.</span><span class="n">randn</span><span class="p">(</span><span class="mi">2000</span><span class="p">,</span> <span class="mi">2000</span><span class="p">)</span>
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
      Y voy a copiar descaradamente la función de Kiko:</p>
    </div>
  </div>
</div>

<div>
  <div>
    <div>
      <div>
        <div class=" highlight hl-ipython3">
          <pre><span class="k">def</span> <span class="nf">busca_min</span><span class="p">(</span><span class="n">malla</span><span class="p">):</span>
    <span class="n">minimosx</span> <span class="o">=</span> <span class="p">[]</span>
    <span class="n">minimosy</span> <span class="o">=</span> <span class="p">[]</span>
    <span class="k">for</span> <span class="n">i</span> <span class="ow">in</span> <span class="nb">range</span><span class="p">(</span><span class="mi">1</span><span class="p">,</span> <span class="n">malla</span><span class="o">.</span><span class="n">shape</span><span class="p">[</span><span class="mi">1</span><span class="p">]</span><span class="o">-</span><span class="mi">1</span><span class="p">):</span>
        <span class="k">for</span> <span class="n">j</span> <span class="ow">in</span> <span class="nb">range</span><span class="p">(</span><span class="mi">1</span><span class="p">,</span> <span class="n">malla</span><span class="o">.</span><span class="n">shape</span><span class="p">[</span><span class="mi"></span><span class="p">]</span><span class="o">-</span><span class="mi">1</span><span class="p">):</span>
            <span class="k">if</span> <span class="p">(</span><span class="n">malla</span><span class="p">[</span><span class="n">j</span><span class="p">,</span> <span class="n">i</span><span class="p">]</span> <span class="o">&lt;</span> <span class="n">malla</span><span class="p">[</span><span class="n">j</span><span class="o">-</span><span class="mi">1</span><span class="p">,</span> <span class="n">i</span><span class="o">-</span><span class="mi">1</span><span class="p">]</span> <span class="ow">and</span>
                <span class="n">malla</span><span class="p">[</span><span class="n">j</span><span class="p">,</span> <span class="n">i</span><span class="p">]</span> <span class="o">&lt;</span> <span class="n">malla</span><span class="p">[</span><span class="n">j</span><span class="o">-</span><span class="mi">1</span><span class="p">,</span> <span class="n">i</span><span class="p">]</span> <span class="ow">and</span>
                <span class="n">malla</span><span class="p">[</span><span class="n">j</span><span class="p">,</span> <span class="n">i</span><span class="p">]</span> <span class="o">&lt;</span> <span class="n">malla</span><span class="p">[</span><span class="n">j</span><span class="o">-</span><span class="mi">1</span><span class="p">,</span> <span class="n">i</span><span class="o">+</span><span class="mi">1</span><span class="p">]</span> <span class="ow">and</span>
                <span class="n">malla</span><span class="p">[</span><span class="n">j</span><span class="p">,</span> <span class="n">i</span><span class="p">]</span> <span class="o">&lt;</span> <span class="n">malla</span><span class="p">[</span><span class="n">j</span><span class="p">,</span> <span class="n">i</span><span class="o">-</span><span class="mi">1</span><span class="p">]</span> <span class="ow">and</span>
                <span class="n">malla</span><span class="p">[</span><span class="n">j</span><span class="p">,</span> <span class="n">i</span><span class="p">]</span> <span class="o">&lt;</span> <span class="n">malla</span><span class="p">[</span><span class="n">j</span><span class="p">,</span> <span class="n">i</span><span class="o">+</span><span class="mi">1</span><span class="p">]</span> <span class="ow">and</span>
                <span class="n">malla</span><span class="p">[</span><span class="n">j</span><span class="p">,</span> <span class="n">i</span><span class="p">]</span> <span class="o">&lt;</span> <span class="n">malla</span><span class="p">[</span><span class="n">j</span><span class="o">+</span><span class="mi">1</span><span class="p">,</span> <span class="n">i</span><span class="o">-</span><span class="mi">1</span><span class="p">]</span> <span class="ow">and</span>
                <span class="n">malla</span><span class="p">[</span><span class="n">j</span><span class="p">,</span> <span class="n">i</span><span class="p">]</span> <span class="o">&lt;</span> <span class="n">malla</span><span class="p">[</span><span class="n">j</span><span class="o">+</span><span class="mi">1</span><span class="p">,</span> <span class="n">i</span><span class="p">]</span> <span class="ow">and</span>
                <span class="n">malla</span><span class="p">[</span><span class="n">j</span><span class="p">,</span> <span class="n">i</span><span class="p">]</span> <span class="o">&lt;</span> <span class="n">malla</span><span class="p">[</span><span class="n">j</span><span class="o">+</span><span class="mi">1</span><span class="p">,</span> <span class="n">i</span><span class="o">+</span><span class="mi">1</span><span class="p">]):</span>
                <span class="n">minimosx</span><span class="o">.</span><span class="n">append</span><span class="p">(</span><span class="n">i</span><span class="p">)</span>
                <span class="n">minimosy</span><span class="o">.</span><span class="n">append</span><span class="p">(</span><span class="n">j</span><span class="p">)</span>

    <span class="k">return</span> <span class="n">np</span><span class="o">.</span><span class="n">array</span><span class="p">(</span><span class="n">minimosx</span><span class="p">),</span> <span class="n">np</span><span class="o">.</span><span class="n">array</span><span class="p">(</span><span class="n">minimosy</span><span class="p">)</span>
</pre>
        </div>
      </div>
    </div>
  </div>
</div>

<div>
  <div>
    <div>
      <div>
        <div class=" highlight hl-ipython3">
          <pre><span class="n">busca_min</span><span class="p">(</span><span class="n">data</span><span class="p">)</span>
</pre>
        </div>
      </div>
    </div>
  </div>
  
  <div>
    <div>
      <div>
        <div>
        </div>
        
        <div>
          <pre>(array([   1,    1,    1, ..., 1998, 1998, 1998]),
 array([   1,    3,   11, ..., 1968, 1977, 1985]))</pre>
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
      <h3 id="Paso-1:-analizar-el-c&#243;digo">
        Paso 1: analizar el c&#243;digo<a class="anchor-link" href="-analizar-el-c&#243;digo">&#182;</a>
      </h3>
      
      <p>
        Lo primero que pensé cuando vi esta función es que no me gustaba nada hacer <code>append</code> a esas dos listas tantas veces. Pero a continuación me pregunté si realmente tendrían tantos elementos... averigüémoslo:
      </p>
    </div>
  </div>
</div>

<div>
  <div>
    <div>
      <div>
        <div class=" highlight hl-ipython3">
          <pre><span class="n">mx</span><span class="p">,</span> <span class="n">my</span> <span class="o">=</span> <span class="n">busca_min</span><span class="p">(</span><span class="n">data</span><span class="p">)</span>
<span class="n">mx</span><span class="o">.</span><span class="n">size</span> <span class="o">/</span> <span class="n">data</span><span class="o">.</span><span class="n">size</span>
</pre>
        </div>
      </div>
    </div>
  </div>
  
  <div>
    <div>
      <div>
        <div>
        </div>
        
        <div>
          <pre>0.11091025</pre>
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
      Tenemos que más de un 10 % de los elementos de la matriz cumplen la condición de ser «mínimos locales», así que no es nada despreciable. Esto en nuestro ejemplo hace <em>un total de más de 400 000 elementos</em>:</p>
    </div>
  </div>
</div>

<div>
  <div>
    <div>
      <div>
        <div class=" highlight hl-ipython3">
          <pre><span class="n">mx</span><span class="o">.</span><span class="n">size</span>
</pre>
        </div>
      </div>
    </div>
  </div>
  
  <div>
    <div>
      <div>
        <div>
        </div>
        
        <div>
          <pre>443641</pre>
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
      Ahora la idea de crear dos listas y añadir los elementos uno a uno me gusta todavía menos, así que voy a cambiar de enfoque. Lo que voy a hacer va a ser crear otro array, de la misma forma que nuestros datos, y almacenar un valor <code>True</code> en aquellos elementos que cumplan la condición de mínimo local. De esta forma cumplo también una de las reglas de oro de Software Carpentry: "<em>Always initialize from data</em>".</p>
    </div>
  </div>
</div>

<div>
  <div>
    <div>
      <div>
        <div class=" highlight hl-ipython3">
          <pre><span class="k">def</span> <span class="nf">busca_min_np</span><span class="p">(</span><span class="n">malla</span><span class="p">):</span>
    <span class="n">minimos</span> <span class="o">=</span> <span class="n">np</span><span class="o">.</span><span class="n">zeros_like</span><span class="p">(</span><span class="n">malla</span><span class="p">,</span> <span class="n">dtype</span><span class="o">=</span><span class="nb">bool</span><span class="p">)</span>
    <span class="k">for</span> <span class="n">i</span> <span class="ow">in</span> <span class="nb">range</span><span class="p">(</span><span class="mi">1</span><span class="p">,</span> <span class="n">malla</span><span class="o">.</span><span class="n">shape</span><span class="p">[</span><span class="mi">1</span><span class="p">]</span><span class="o">-</span><span class="mi">1</span><span class="p">):</span>
        <span class="k">for</span> <span class="n">j</span> <span class="ow">in</span> <span class="nb">range</span><span class="p">(</span><span class="mi">1</span><span class="p">,</span> <span class="n">malla</span><span class="o">.</span><span class="n">shape</span><span class="p">[</span><span class="mi"></span><span class="p">]</span><span class="o">-</span><span class="mi">1</span><span class="p">):</span>
            <span class="k">if</span> <span class="p">(</span><span class="n">malla</span><span class="p">[</span><span class="n">j</span><span class="p">,</span> <span class="n">i</span><span class="p">]</span> <span class="o">&lt;</span> <span class="n">malla</span><span class="p">[</span><span class="n">j</span><span class="o">-</span><span class="mi">1</span><span class="p">,</span> <span class="n">i</span><span class="o">-</span><span class="mi">1</span><span class="p">]</span> <span class="ow">and</span>
                <span class="n">malla</span><span class="p">[</span><span class="n">j</span><span class="p">,</span> <span class="n">i</span><span class="p">]</span> <span class="o">&lt;</span> <span class="n">malla</span><span class="p">[</span><span class="n">j</span><span class="o">-</span><span class="mi">1</span><span class="p">,</span> <span class="n">i</span><span class="p">]</span> <span class="ow">and</span>
                <span class="n">malla</span><span class="p">[</span><span class="n">j</span><span class="p">,</span> <span class="n">i</span><span class="p">]</span> <span class="o">&lt;</span> <span class="n">malla</span><span class="p">[</span><span class="n">j</span><span class="o">-</span><span class="mi">1</span><span class="p">,</span> <span class="n">i</span><span class="o">+</span><span class="mi">1</span><span class="p">]</span> <span class="ow">and</span>
                <span class="n">malla</span><span class="p">[</span><span class="n">j</span><span class="p">,</span> <span class="n">i</span><span class="p">]</span> <span class="o">&lt;</span> <span class="n">malla</span><span class="p">[</span><span class="n">j</span><span class="p">,</span> <span class="n">i</span><span class="o">-</span><span class="mi">1</span><span class="p">]</span> <span class="ow">and</span>
                <span class="n">malla</span><span class="p">[</span><span class="n">j</span><span class="p">,</span> <span class="n">i</span><span class="p">]</span> <span class="o">&lt;</span> <span class="n">malla</span><span class="p">[</span><span class="n">j</span><span class="p">,</span> <span class="n">i</span><span class="o">+</span><span class="mi">1</span><span class="p">]</span> <span class="ow">and</span>
                <span class="n">malla</span><span class="p">[</span><span class="n">j</span><span class="p">,</span> <span class="n">i</span><span class="p">]</span> <span class="o">&lt;</span> <span class="n">malla</span><span class="p">[</span><span class="n">j</span><span class="o">+</span><span class="mi">1</span><span class="p">,</span> <span class="n">i</span><span class="o">-</span><span class="mi">1</span><span class="p">]</span> <span class="ow">and</span>
                <span class="n">malla</span><span class="p">[</span><span class="n">j</span><span class="p">,</span> <span class="n">i</span><span class="p">]</span> <span class="o">&lt;</span> <span class="n">malla</span><span class="p">[</span><span class="n">j</span><span class="o">+</span><span class="mi">1</span><span class="p">,</span> <span class="n">i</span><span class="p">]</span> <span class="ow">and</span>
                <span class="n">malla</span><span class="p">[</span><span class="n">j</span><span class="p">,</span> <span class="n">i</span><span class="p">]</span> <span class="o">&lt;</span> <span class="n">malla</span><span class="p">[</span><span class="n">j</span><span class="o">+</span><span class="mi">1</span><span class="p">,</span> <span class="n">i</span><span class="o">+</span><span class="mi">1</span><span class="p">]):</span>
                <span class="n">minimos</span><span class="p">[</span><span class="n">i</span><span class="p">,</span> <span class="n">j</span><span class="p">]</span> <span class="o">=</span> <span class="k">True</span>

    <span class="k">return</span> <span class="n">np</span><span class="o">.</span><span class="n">nonzero</span><span class="p">(</span><span class="n">minimos</span><span class="p">)</span>
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
      Encima puedo aprovechar la estupenda función <code>nonzero</code> de NumPy. Compruebo que las salidas son iguales:</p>
    </div>
  </div>
</div>

<div>
  <div>
    <div>
      <div>
        <div class=" highlight hl-ipython3">
          <pre><span class="n">np</span><span class="o">.</span><span class="n">testing</span><span class="o">.</span><span class="n">assert_array_equal</span><span class="p">(</span><span class="n">busca_min</span><span class="p">(</span><span class="n">data</span><span class="p">)[</span><span class="mi"></span><span class="p">],</span> <span class="n">busca_min_np</span><span class="p">(</span><span class="n">data</span><span class="p">)[</span><span class="mi"></span><span class="p">])</span>
<span class="n">np</span><span class="o">.</span><span class="n">testing</span><span class="o">.</span><span class="n">assert_array_equal</span><span class="p">(</span><span class="n">busca_min</span><span class="p">(</span><span class="n">data</span><span class="p">)[</span><span class="mi">1</span><span class="p">],</span> <span class="n">busca_min_np</span><span class="p">(</span><span class="n">data</span><span class="p">)[</span><span class="mi">1</span><span class="p">])</span>
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
      Y evalúo los rendimientos:</p>
    </div>
  </div>
</div>

<div>
  <div>
    <div>
      <div>
        <div class=" highlight hl-ipython3">
          <pre><span class="o">%</span><span class="k">timeit</span> busca_min(data)
</pre>
        </div>
      </div>
    </div>
  </div>
  
  <div>
    <div>
      <div>
        <div>
        </div>
        
        <div>
          <pre>1 loops, best of 3: 4.75 s per loop
</pre>
        </div>
      </div>
    </div>
  </div>
</div>

<div>
  <div>
    <div>
      <div>
        <div class=" highlight hl-ipython3">
          <pre><span class="o">%</span><span class="k">timeit</span> busca_min_np(data)
</pre>
        </div>
      </div>
    </div>
  </div>
  
  <div>
    <div>
      <div>
        <div>
        </div>
        
        <div>
          <pre>1 loops, best of 3: 4.62 s per loop
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
      Parece que los tiempos son más o menos parecidos, pero al menos ya no tengo dos objetos en memoria que van a crecer de manera aleatoria. Vamos a ver ahora cómo nos puede ayudar numba a acelerar este código.</p>
    </div>
  </div>
</div>

<div>
  <div>
  </div>
  
  <div>
    <div>
      <h3 id="Paso-2:-aplicando-numba.jit(nopython=True)">
        Paso 2: aplicando <code>numba.jit(nopython=True)</code><a class="anchor-link" href="-aplicando-numba.jit(nopython=True)">&#182;</a>
      </h3>
      
      <p>
        Como hemos dicho antes, vamos a forzar que numba funcione en modo <em>nopython</em> para garantizar que obtenemos una mejora en el rendimiento. Si intentamos compilar la función definida en primer lugar va a fallar, porque ya hemos dicho más arriba que una de las condiciones es que <em>no se puede asignar memoria a objetos nuevos</em>:
      </p>
    </div>
  </div>
</div>

<div>
  <div>
    <div>
      <div>
        <div class=" highlight hl-ipython3">
          <pre><span class="n">busca_min_jit</span> <span class="o">=</span> <span class="n">numba</span><span class="o">.</span><span class="n">jit</span><span class="p">(</span><span class="n">nopython</span><span class="o">=</span><span class="k">True</span><span class="p">)(</span><span class="n">busca_min</span><span class="p">)</span>
<span class="n">busca_min_jit</span><span class="p">(</span><span class="n">data</span><span class="p">)</span>
</pre>
        </div>
      </div>
    </div>
  </div>
  
  <div>
    <div>
      <div>
        <div>
        </div>
        
        <div>
          <pre>
<span class="ansired">---------------------------------------------------------------------------</span>
<span class="ansired">NotImplementedError</span>                       Traceback (most recent call last)
<span class="ansigreen">&lt;ipython-input-14-3ca127791a45&gt;</span> in <span class="ansicyan">&lt;module&gt;</span><span class="ansiblue">()</span>
<span class="ansigreen">      1</span> busca_min_jit <span class="ansiyellow">=</span> numba<span class="ansiyellow">.</span>jit<span class="ansiyellow">(</span>nopython<span class="ansiyellow">=</span><span class="ansigreen">True</span><span class="ansiyellow">)</span><span class="ansiyellow">(</span>busca_min<span class="ansiyellow">)</span><span class="ansiyellow"></span>
<span class="ansigreen">----&gt; 2</span><span class="ansiyellow"> </span>busca_min_jit<span class="ansiyellow">(</span>data<span class="ansiyellow">)</span><span class="ansiyellow"></span>

<span class="ansigreen">/home/juanlu/.miniconda3/envs/py34/lib/python3.4/site-packages/numba/dispatcher.py</span> in <span class="ansicyan">_compile_for_args</span><span class="ansiblue">(self, *args, **kws)</span>
<span class="ansigreen">    155</span>         <span class="ansigreen">assert</span> <span class="ansigreen">not</span> kws<span class="ansiyellow"></span>
<span class="ansigreen">    156</span>         sig <span class="ansiyellow">=</span> tuple<span class="ansiyellow">(</span><span class="ansiyellow">[</span>self<span class="ansiyellow">.</span>typeof_pyval<span class="ansiyellow">(</span>a<span class="ansiyellow">)</span> <span class="ansigreen">for</span> a <span class="ansigreen">in</span> args<span class="ansiyellow">]</span><span class="ansiyellow">)</span><span class="ansiyellow"></span>
<span class="ansigreen">--&gt; 157</span><span class="ansiyellow">         </span><span class="ansigreen">return</span> self<span class="ansiyellow">.</span>compile<span class="ansiyellow">(</span>sig<span class="ansiyellow">)</span><span class="ansiyellow"></span>
<span class="ansigreen">    158</span> <span class="ansiyellow"></span>
<span class="ansigreen">    159</span>     <span class="ansigreen">def</span> inspect_types<span class="ansiyellow">(</span>self<span class="ansiyellow">,</span> file<span class="ansiyellow">=</span><span class="ansigreen">None</span><span class="ansiyellow">)</span><span class="ansiyellow">:</span><span class="ansiyellow"></span>

<span class="ansigreen">/home/juanlu/.miniconda3/envs/py34/lib/python3.4/site-packages/numba/dispatcher.py</span> in <span class="ansicyan">compile</span><span class="ansiblue">(self, sig)</span>
<span class="ansigreen">    275</span>                                           self<span class="ansiyellow">.</span>py_func<span class="ansiyellow">,</span><span class="ansiyellow"></span>
<span class="ansigreen">    276</span>                                           args<span class="ansiyellow">=</span>args<span class="ansiyellow">,</span> return_type<span class="ansiyellow">=</span>return_type<span class="ansiyellow">,</span><span class="ansiyellow"></span>
<span class="ansigreen">--&gt; 277</span><span class="ansiyellow">                                           flags=flags, locals=self.locals)
</span><span class="ansigreen">    278</span> <span class="ansiyellow"></span>
<span class="ansigreen">    279</span>             <span class="ansired"># Check typing error if object mode is used</span><span class="ansiyellow"></span><span class="ansiyellow"></span>

<span class="ansigreen">/home/juanlu/.miniconda3/envs/py34/lib/python3.4/site-packages/numba/compiler.py</span> in <span class="ansicyan">compile_extra</span><span class="ansiblue">(typingctx, targetctx, func, args, return_type, flags, locals, library)</span>
<span class="ansigreen">    545</span>     pipeline = Pipeline(typingctx, targetctx, library,
<span class="ansigreen">    546</span>                         args, return_type, flags, locals)
<span class="ansigreen">--&gt; 547</span><span class="ansiyellow">     </span><span class="ansigreen">return</span> pipeline<span class="ansiyellow">.</span>compile_extra<span class="ansiyellow">(</span>func<span class="ansiyellow">)</span><span class="ansiyellow"></span>
<span class="ansigreen">    548</span> <span class="ansiyellow"></span>
<span class="ansigreen">    549</span> <span class="ansiyellow"></span>

<span class="ansigreen">/home/juanlu/.miniconda3/envs/py34/lib/python3.4/site-packages/numba/compiler.py</span> in <span class="ansicyan">compile_extra</span><span class="ansiblue">(self, func)</span>
<span class="ansigreen">    291</span>                 <span class="ansigreen">raise</span> e<span class="ansiyellow"></span>
<span class="ansigreen">    292</span> <span class="ansiyellow"></span>
<span class="ansigreen">--&gt; 293</span><span class="ansiyellow">         </span><span class="ansigreen">return</span> self<span class="ansiyellow">.</span>compile_bytecode<span class="ansiyellow">(</span>bc<span class="ansiyellow">,</span> func_attr<span class="ansiyellow">=</span>self<span class="ansiyellow">.</span>func_attr<span class="ansiyellow">)</span><span class="ansiyellow"></span>
<span class="ansigreen">    294</span> <span class="ansiyellow"></span>
<span class="ansigreen">    295</span>     def compile_bytecode(self, bc, lifted=(),

<span class="ansigreen">/home/juanlu/.miniconda3/envs/py34/lib/python3.4/site-packages/numba/compiler.py</span> in <span class="ansicyan">compile_bytecode</span><span class="ansiblue">(self, bc, lifted, func_attr)</span>
<span class="ansigreen">    299</span>         self<span class="ansiyellow">.</span>lifted <span class="ansiyellow">=</span> lifted<span class="ansiyellow"></span>
<span class="ansigreen">    300</span>         self<span class="ansiyellow">.</span>func_attr <span class="ansiyellow">=</span> func_attr<span class="ansiyellow"></span>
<span class="ansigreen">--&gt; 301</span><span class="ansiyellow">         </span><span class="ansigreen">return</span> self<span class="ansiyellow">.</span>_compile_bytecode<span class="ansiyellow">(</span><span class="ansiyellow">)</span><span class="ansiyellow"></span>
<span class="ansigreen">    302</span> <span class="ansiyellow"></span>
<span class="ansigreen">    303</span>     <span class="ansigreen">def</span> compile_internal<span class="ansiyellow">(</span>self<span class="ansiyellow">,</span> bc<span class="ansiyellow">,</span> func_attr<span class="ansiyellow">=</span>DEFAULT_FUNCTION_ATTRIBUTES<span class="ansiyellow">)</span><span class="ansiyellow">:</span><span class="ansiyellow"></span>

<span class="ansigreen">/home/juanlu/.miniconda3/envs/py34/lib/python3.4/site-packages/numba/compiler.py</span> in <span class="ansicyan">_compile_bytecode</span><span class="ansiblue">(self)</span>
<span class="ansigreen">    532</span> <span class="ansiyellow"></span>
<span class="ansigreen">    533</span>         pm<span class="ansiyellow">.</span>finalize<span class="ansiyellow">(</span><span class="ansiyellow">)</span><span class="ansiyellow"></span>
<span class="ansigreen">--&gt; 534</span><span class="ansiyellow">         </span><span class="ansigreen">return</span> pm<span class="ansiyellow">.</span>run<span class="ansiyellow">(</span>self<span class="ansiyellow">.</span>status<span class="ansiyellow">)</span><span class="ansiyellow"></span>
<span class="ansigreen">    535</span> <span class="ansiyellow"></span>
<span class="ansigreen">    536</span> <span class="ansiyellow"></span>

<span class="ansigreen">/home/juanlu/.miniconda3/envs/py34/lib/python3.4/site-packages/numba/compiler.py</span> in <span class="ansicyan">run</span><span class="ansiblue">(self, status)</span>
<span class="ansigreen">    189</span>                     <span class="ansired"># No more fallback pipelines?</span><span class="ansiyellow"></span><span class="ansiyellow"></span>
<span class="ansigreen">    190</span>                     <span class="ansigreen">if</span> is_final_pipeline<span class="ansiyellow">:</span><span class="ansiyellow"></span>
<span class="ansigreen">--&gt; 191</span><span class="ansiyellow">                         </span><span class="ansigreen">raise</span> patched_exception<span class="ansiyellow"></span>
<span class="ansigreen">    192</span>                     <span class="ansired"># Go to next fallback pipeline</span><span class="ansiyellow"></span><span class="ansiyellow"></span>
<span class="ansigreen">    193</span>                     <span class="ansigreen">else</span><span class="ansiyellow">:</span><span class="ansiyellow"></span>

<span class="ansigreen">/home/juanlu/.miniconda3/envs/py34/lib/python3.4/site-packages/numba/compiler.py</span> in <span class="ansicyan">run</span><span class="ansiblue">(self, status)</span>
<span class="ansigreen">    181</span>             <span class="ansigreen">for</span> stage<span class="ansiyellow">,</span> stage_name <span class="ansigreen">in</span> self<span class="ansiyellow">.</span>pipeline_stages<span class="ansiyellow">[</span>pipeline_name<span class="ansiyellow">]</span><span class="ansiyellow">:</span><span class="ansiyellow"></span>
<span class="ansigreen">    182</span>                 <span class="ansigreen">try</span><span class="ansiyellow">:</span><span class="ansiyellow"></span>
<span class="ansigreen">--&gt; 183</span><span class="ansiyellow">                     </span>res <span class="ansiyellow">=</span> stage<span class="ansiyellow">(</span><span class="ansiyellow">)</span><span class="ansiyellow"></span>
<span class="ansigreen">    184</span>                 <span class="ansigreen">except</span> _EarlyPipelineCompletion <span class="ansigreen">as</span> e<span class="ansiyellow">:</span><span class="ansiyellow"></span>
<span class="ansigreen">    185</span>                     <span class="ansigreen">return</span> e<span class="ansiyellow">.</span>result<span class="ansiyellow"></span>

<span class="ansigreen">/home/juanlu/.miniconda3/envs/py34/lib/python3.4/site-packages/numba/compiler.py</span> in <span class="ansicyan">stage_nopython_frontend</span><span class="ansiblue">(self)</span>
<span class="ansigreen">    387</span>                 self<span class="ansiyellow">.</span>args<span class="ansiyellow">,</span><span class="ansiyellow"></span>
<span class="ansigreen">    388</span>                 self<span class="ansiyellow">.</span>return_type<span class="ansiyellow">,</span><span class="ansiyellow"></span>
<span class="ansigreen">--&gt; 389</span><span class="ansiyellow">                 self.locals)
</span><span class="ansigreen">    390</span> <span class="ansiyellow"></span>
<span class="ansigreen">    391</span>         with self.fallback_context(';Function "%s" has invalid return type';

<span class="ansigreen">/home/juanlu/.miniconda3/envs/py34/lib/python3.4/site-packages/numba/compiler.py</span> in <span class="ansicyan">type_inference_stage</span><span class="ansiblue">(typingctx, interp, args, return_type, locals)</span>
<span class="ansigreen">    662</span>         infer<span class="ansiyellow">.</span>seed_type<span class="ansiyellow">(</span>k<span class="ansiyellow">,</span> v<span class="ansiyellow">)</span><span class="ansiyellow"></span>
<span class="ansigreen">    663</span> <span class="ansiyellow"></span>
<span class="ansigreen">--&gt; 664</span><span class="ansiyellow">     </span>infer<span class="ansiyellow">.</span>build_constrain<span class="ansiyellow">(</span><span class="ansiyellow">)</span><span class="ansiyellow"></span>
<span class="ansigreen">    665</span>     infer<span class="ansiyellow">.</span>propagate<span class="ansiyellow">(</span><span class="ansiyellow">)</span><span class="ansiyellow"></span>
<span class="ansigreen">    666</span>     typemap<span class="ansiyellow">,</span> restype<span class="ansiyellow">,</span> calltypes <span class="ansiyellow">=</span> infer<span class="ansiyellow">.</span>unify<span class="ansiyellow">(</span><span class="ansiyellow">)</span><span class="ansiyellow"></span>

<span class="ansigreen">/home/juanlu/.miniconda3/envs/py34/lib/python3.4/site-packages/numba/typeinfer.py</span> in <span class="ansicyan">build_constrain</span><span class="ansiblue">(self)</span>
<span class="ansigreen">    375</span>         <span class="ansigreen">for</span> blk <span class="ansigreen">in</span> utils<span class="ansiyellow">.</span>itervalues<span class="ansiyellow">(</span>self<span class="ansiyellow">.</span>blocks<span class="ansiyellow">)</span><span class="ansiyellow">:</span><span class="ansiyellow"></span>
<span class="ansigreen">    376</span>             <span class="ansigreen">for</span> inst <span class="ansigreen">in</span> blk<span class="ansiyellow">.</span>body<span class="ansiyellow">:</span><span class="ansiyellow"></span>
<span class="ansigreen">--&gt; 377</span><span class="ansiyellow">                 </span>self<span class="ansiyellow">.</span>constrain_statement<span class="ansiyellow">(</span>inst<span class="ansiyellow">)</span><span class="ansiyellow"></span>
<span class="ansigreen">    378</span> <span class="ansiyellow"></span>
<span class="ansigreen">    379</span>     <span class="ansigreen">def</span> propagate<span class="ansiyellow">(</span>self<span class="ansiyellow">)</span><span class="ansiyellow">:</span><span class="ansiyellow"></span>

<span class="ansigreen">/home/juanlu/.miniconda3/envs/py34/lib/python3.4/site-packages/numba/typeinfer.py</span> in <span class="ansicyan">constrain_statement</span><span class="ansiblue">(self, inst)</span>
<span class="ansigreen">    480</span>     <span class="ansigreen">def</span> constrain_statement<span class="ansiyellow">(</span>self<span class="ansiyellow">,</span> inst<span class="ansiyellow">)</span><span class="ansiyellow">:</span><span class="ansiyellow"></span>
<span class="ansigreen">    481</span>         <span class="ansigreen">if</span> isinstance<span class="ansiyellow">(</span>inst<span class="ansiyellow">,</span> ir<span class="ansiyellow">.</span>Assign<span class="ansiyellow">)</span><span class="ansiyellow">:</span><span class="ansiyellow"></span>
<span class="ansigreen">--&gt; 482</span><span class="ansiyellow">             </span>self<span class="ansiyellow">.</span>typeof_assign<span class="ansiyellow">(</span>inst<span class="ansiyellow">)</span><span class="ansiyellow"></span>
<span class="ansigreen">    483</span>         <span class="ansigreen">elif</span> isinstance<span class="ansiyellow">(</span>inst<span class="ansiyellow">,</span> ir<span class="ansiyellow">.</span>SetItem<span class="ansiyellow">)</span><span class="ansiyellow">:</span><span class="ansiyellow"></span>
<span class="ansigreen">    484</span>             self<span class="ansiyellow">.</span>typeof_setitem<span class="ansiyellow">(</span>inst<span class="ansiyellow">)</span><span class="ansiyellow"></span>

<span class="ansigreen">/home/juanlu/.miniconda3/envs/py34/lib/python3.4/site-packages/numba/typeinfer.py</span> in <span class="ansicyan">typeof_assign</span><span class="ansiblue">(self, inst)</span>
<span class="ansigreen">    514</span>             self<span class="ansiyellow">.</span>typeof_global<span class="ansiyellow">(</span>inst<span class="ansiyellow">,</span> inst<span class="ansiyellow">.</span>target<span class="ansiyellow">,</span> value<span class="ansiyellow">)</span><span class="ansiyellow"></span>
<span class="ansigreen">    515</span>         <span class="ansigreen">elif</span> isinstance<span class="ansiyellow">(</span>value<span class="ansiyellow">,</span> ir<span class="ansiyellow">.</span>Expr<span class="ansiyellow">)</span><span class="ansiyellow">:</span><span class="ansiyellow"></span>
<span class="ansigreen">--&gt; 516</span><span class="ansiyellow">             </span>self<span class="ansiyellow">.</span>typeof_expr<span class="ansiyellow">(</span>inst<span class="ansiyellow">,</span> inst<span class="ansiyellow">.</span>target<span class="ansiyellow">,</span> value<span class="ansiyellow">)</span><span class="ansiyellow"></span>
<span class="ansigreen">    517</span>         <span class="ansigreen">else</span><span class="ansiyellow">:</span><span class="ansiyellow"></span>
<span class="ansigreen">    518</span>             <span class="ansigreen">raise</span> NotImplementedError<span class="ansiyellow">(</span>type<span class="ansiyellow">(</span>value<span class="ansiyellow">)</span><span class="ansiyellow">,</span> value<span class="ansiyellow">)</span><span class="ansiyellow"></span>

<span class="ansigreen">/home/juanlu/.miniconda3/envs/py34/lib/python3.4/site-packages/numba/typeinfer.py</span> in <span class="ansicyan">typeof_expr</span><span class="ansiblue">(self, inst, target, expr)</span>
<span class="ansigreen">    618</span>                                              loc=inst.loc))
<span class="ansigreen">    619</span>         <span class="ansigreen">else</span><span class="ansiyellow">:</span><span class="ansiyellow"></span>
<span class="ansigreen">--&gt; 620</span><span class="ansiyellow">             </span><span class="ansigreen">raise</span> NotImplementedError<span class="ansiyellow">(</span>type<span class="ansiyellow">(</span>expr<span class="ansiyellow">)</span><span class="ansiyellow">,</span> expr<span class="ansiyellow">)</span><span class="ansiyellow"></span>
<span class="ansigreen">    621</span> <span class="ansiyellow"></span>
<span class="ansigreen">    622</span>     <span class="ansigreen">def</span> typeof_call<span class="ansiyellow">(</span>self<span class="ansiyellow">,</span> inst<span class="ansiyellow">,</span> target<span class="ansiyellow">,</span> call<span class="ansiyellow">)</span><span class="ansiyellow">:</span><span class="ansiyellow"></span>

<span class="ansired">NotImplementedError</span>: Failed at nopython (nopython frontend)
(&lt;class ';numba.ir.Expr';&gt;, build_list(items=[]))</pre>
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
      En este caso la traza es inservible y especificar los tipos de entrada no va a ayudar. Solo para verificar, vamos a ver qué pasa con el rendimiento si no forzamos el modo estricto:</p>
    </div>
  </div>
</div>

<div>
  <div>
    <div>
      <div>
        <div class=" highlight hl-ipython3">
          <pre><span class="n">busca_min_jit_object</span> <span class="o">=</span> <span class="n">numba</span><span class="o">.</span><span class="n">jit</span><span class="p">()(</span><span class="n">busca_min</span><span class="p">)</span>
</pre>
        </div>
      </div>
    </div>
  </div>
</div>

<div>
  <div>
    <div>
      <div>
        <div class=" highlight hl-ipython3">
          <pre><span class="o">%</span><span class="k">timeit</span> busca_min_jit_object(data)
</pre>
        </div>
      </div>
    </div>
  </div>
  
  <div>
    <div>
      <div>
        <div>
        </div>
        
        <div>
          <pre>1 loops, best of 3: 4.32 s per loop
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
      Pocas ganancias respecto a la función sin compilar. ¿Qué pasa si intentamos lo mismo con la segunda función?</p>
    </div>
  </div>
</div>

<div>
  <div>
    <div>
      <div>
        <div class=" highlight hl-ipython3">
          <pre><span class="n">busca_min_np_jit</span> <span class="o">=</span> <span class="n">numba</span><span class="o">.</span><span class="n">jit</span><span class="p">(</span><span class="n">nopython</span><span class="o">=</span><span class="k">True</span><span class="p">)(</span><span class="n">busca_min_np</span><span class="p">)</span>
<span class="n">busca_min_np_jit</span><span class="p">(</span><span class="n">data</span><span class="p">)</span>
</pre>
        </div>
      </div>
    </div>
  </div>
  
  <div>
    <div>
      <div>
        <div>
        </div>
        
        <div>
          <pre>
<span class="ansired">---------------------------------------------------------------------------</span>
<span class="ansired">UntypedAttributeError</span>                     Traceback (most recent call last)
<span class="ansigreen">&lt;ipython-input-17-bb9282bb2bfc&gt;</span> in <span class="ansicyan">&lt;module&gt;</span><span class="ansiblue">()</span>
<span class="ansigreen">      1</span> busca_min_np_jit <span class="ansiyellow">=</span> numba<span class="ansiyellow">.</span>jit<span class="ansiyellow">(</span>nopython<span class="ansiyellow">=</span><span class="ansigreen">True</span><span class="ansiyellow">)</span><span class="ansiyellow">(</span>busca_min_np<span class="ansiyellow">)</span><span class="ansiyellow"></span>
<span class="ansigreen">----&gt; 2</span><span class="ansiyellow"> </span>busca_min_np_jit<span class="ansiyellow">(</span>data<span class="ansiyellow">)</span><span class="ansiyellow"></span>

<span class="ansigreen">/home/juanlu/.miniconda3/envs/py34/lib/python3.4/site-packages/numba/dispatcher.py</span> in <span class="ansicyan">_compile_for_args</span><span class="ansiblue">(self, *args, **kws)</span>
<span class="ansigreen">    155</span>         <span class="ansigreen">assert</span> <span class="ansigreen">not</span> kws<span class="ansiyellow"></span>
<span class="ansigreen">    156</span>         sig <span class="ansiyellow">=</span> tuple<span class="ansiyellow">(</span><span class="ansiyellow">[</span>self<span class="ansiyellow">.</span>typeof_pyval<span class="ansiyellow">(</span>a<span class="ansiyellow">)</span> <span class="ansigreen">for</span> a <span class="ansigreen">in</span> args<span class="ansiyellow">]</span><span class="ansiyellow">)</span><span class="ansiyellow"></span>
<span class="ansigreen">--&gt; 157</span><span class="ansiyellow">         </span><span class="ansigreen">return</span> self<span class="ansiyellow">.</span>compile<span class="ansiyellow">(</span>sig<span class="ansiyellow">)</span><span class="ansiyellow"></span>
<span class="ansigreen">    158</span> <span class="ansiyellow"></span>
<span class="ansigreen">    159</span>     <span class="ansigreen">def</span> inspect_types<span class="ansiyellow">(</span>self<span class="ansiyellow">,</span> file<span class="ansiyellow">=</span><span class="ansigreen">None</span><span class="ansiyellow">)</span><span class="ansiyellow">:</span><span class="ansiyellow"></span>

<span class="ansigreen">/home/juanlu/.miniconda3/envs/py34/lib/python3.4/site-packages/numba/dispatcher.py</span> in <span class="ansicyan">compile</span><span class="ansiblue">(self, sig)</span>
<span class="ansigreen">    275</span>                                           self<span class="ansiyellow">.</span>py_func<span class="ansiyellow">,</span><span class="ansiyellow"></span>
<span class="ansigreen">    276</span>                                           args<span class="ansiyellow">=</span>args<span class="ansiyellow">,</span> return_type<span class="ansiyellow">=</span>return_type<span class="ansiyellow">,</span><span class="ansiyellow"></span>
<span class="ansigreen">--&gt; 277</span><span class="ansiyellow">                                           flags=flags, locals=self.locals)
</span><span class="ansigreen">    278</span> <span class="ansiyellow"></span>
<span class="ansigreen">    279</span>             <span class="ansired"># Check typing error if object mode is used</span><span class="ansiyellow"></span><span class="ansiyellow"></span>

<span class="ansigreen">/home/juanlu/.miniconda3/envs/py34/lib/python3.4/site-packages/numba/compiler.py</span> in <span class="ansicyan">compile_extra</span><span class="ansiblue">(typingctx, targetctx, func, args, return_type, flags, locals, library)</span>
<span class="ansigreen">    545</span>     pipeline = Pipeline(typingctx, targetctx, library,
<span class="ansigreen">    546</span>                         args, return_type, flags, locals)
<span class="ansigreen">--&gt; 547</span><span class="ansiyellow">     </span><span class="ansigreen">return</span> pipeline<span class="ansiyellow">.</span>compile_extra<span class="ansiyellow">(</span>func<span class="ansiyellow">)</span><span class="ansiyellow"></span>
<span class="ansigreen">    548</span> <span class="ansiyellow"></span>
<span class="ansigreen">    549</span> <span class="ansiyellow"></span>

<span class="ansigreen">/home/juanlu/.miniconda3/envs/py34/lib/python3.4/site-packages/numba/compiler.py</span> in <span class="ansicyan">compile_extra</span><span class="ansiblue">(self, func)</span>
<span class="ansigreen">    291</span>                 <span class="ansigreen">raise</span> e<span class="ansiyellow"></span>
<span class="ansigreen">    292</span> <span class="ansiyellow"></span>
<span class="ansigreen">--&gt; 293</span><span class="ansiyellow">         </span><span class="ansigreen">return</span> self<span class="ansiyellow">.</span>compile_bytecode<span class="ansiyellow">(</span>bc<span class="ansiyellow">,</span> func_attr<span class="ansiyellow">=</span>self<span class="ansiyellow">.</span>func_attr<span class="ansiyellow">)</span><span class="ansiyellow"></span>
<span class="ansigreen">    294</span> <span class="ansiyellow"></span>
<span class="ansigreen">    295</span>     def compile_bytecode(self, bc, lifted=(),

<span class="ansigreen">/home/juanlu/.miniconda3/envs/py34/lib/python3.4/site-packages/numba/compiler.py</span> in <span class="ansicyan">compile_bytecode</span><span class="ansiblue">(self, bc, lifted, func_attr)</span>
<span class="ansigreen">    299</span>         self<span class="ansiyellow">.</span>lifted <span class="ansiyellow">=</span> lifted<span class="ansiyellow"></span>
<span class="ansigreen">    300</span>         self<span class="ansiyellow">.</span>func_attr <span class="ansiyellow">=</span> func_attr<span class="ansiyellow"></span>
<span class="ansigreen">--&gt; 301</span><span class="ansiyellow">         </span><span class="ansigreen">return</span> self<span class="ansiyellow">.</span>_compile_bytecode<span class="ansiyellow">(</span><span class="ansiyellow">)</span><span class="ansiyellow"></span>
<span class="ansigreen">    302</span> <span class="ansiyellow"></span>
<span class="ansigreen">    303</span>     <span class="ansigreen">def</span> compile_internal<span class="ansiyellow">(</span>self<span class="ansiyellow">,</span> bc<span class="ansiyellow">,</span> func_attr<span class="ansiyellow">=</span>DEFAULT_FUNCTION_ATTRIBUTES<span class="ansiyellow">)</span><span class="ansiyellow">:</span><span class="ansiyellow"></span>

<span class="ansigreen">/home/juanlu/.miniconda3/envs/py34/lib/python3.4/site-packages/numba/compiler.py</span> in <span class="ansicyan">_compile_bytecode</span><span class="ansiblue">(self)</span>
<span class="ansigreen">    532</span> <span class="ansiyellow"></span>
<span class="ansigreen">    533</span>         pm<span class="ansiyellow">.</span>finalize<span class="ansiyellow">(</span><span class="ansiyellow">)</span><span class="ansiyellow"></span>
<span class="ansigreen">--&gt; 534</span><span class="ansiyellow">         </span><span class="ansigreen">return</span> pm<span class="ansiyellow">.</span>run<span class="ansiyellow">(</span>self<span class="ansiyellow">.</span>status<span class="ansiyellow">)</span><span class="ansiyellow"></span>
<span class="ansigreen">    535</span> <span class="ansiyellow"></span>
<span class="ansigreen">    536</span> <span class="ansiyellow"></span>

<span class="ansigreen">/home/juanlu/.miniconda3/envs/py34/lib/python3.4/site-packages/numba/compiler.py</span> in <span class="ansicyan">run</span><span class="ansiblue">(self, status)</span>
<span class="ansigreen">    189</span>                     <span class="ansired"># No more fallback pipelines?</span><span class="ansiyellow"></span><span class="ansiyellow"></span>
<span class="ansigreen">    190</span>                     <span class="ansigreen">if</span> is_final_pipeline<span class="ansiyellow">:</span><span class="ansiyellow"></span>
<span class="ansigreen">--&gt; 191</span><span class="ansiyellow">                         </span><span class="ansigreen">raise</span> patched_exception<span class="ansiyellow"></span>
<span class="ansigreen">    192</span>                     <span class="ansired"># Go to next fallback pipeline</span><span class="ansiyellow"></span><span class="ansiyellow"></span>
<span class="ansigreen">    193</span>                     <span class="ansigreen">else</span><span class="ansiyellow">:</span><span class="ansiyellow"></span>

<span class="ansigreen">/home/juanlu/.miniconda3/envs/py34/lib/python3.4/site-packages/numba/compiler.py</span> in <span class="ansicyan">run</span><span class="ansiblue">(self, status)</span>
<span class="ansigreen">    181</span>             <span class="ansigreen">for</span> stage<span class="ansiyellow">,</span> stage_name <span class="ansigreen">in</span> self<span class="ansiyellow">.</span>pipeline_stages<span class="ansiyellow">[</span>pipeline_name<span class="ansiyellow">]</span><span class="ansiyellow">:</span><span class="ansiyellow"></span>
<span class="ansigreen">    182</span>                 <span class="ansigreen">try</span><span class="ansiyellow">:</span><span class="ansiyellow"></span>
<span class="ansigreen">--&gt; 183</span><span class="ansiyellow">                     </span>res <span class="ansiyellow">=</span> stage<span class="ansiyellow">(</span><span class="ansiyellow">)</span><span class="ansiyellow"></span>
<span class="ansigreen">    184</span>                 <span class="ansigreen">except</span> _EarlyPipelineCompletion <span class="ansigreen">as</span> e<span class="ansiyellow">:</span><span class="ansiyellow"></span>
<span class="ansigreen">    185</span>                     <span class="ansigreen">return</span> e<span class="ansiyellow">.</span>result<span class="ansiyellow"></span>

<span class="ansigreen">/home/juanlu/.miniconda3/envs/py34/lib/python3.4/site-packages/numba/compiler.py</span> in <span class="ansicyan">stage_nopython_frontend</span><span class="ansiblue">(self)</span>
<span class="ansigreen">    387</span>                 self<span class="ansiyellow">.</span>args<span class="ansiyellow">,</span><span class="ansiyellow"></span>
<span class="ansigreen">    388</span>                 self<span class="ansiyellow">.</span>return_type<span class="ansiyellow">,</span><span class="ansiyellow"></span>
<span class="ansigreen">--&gt; 389</span><span class="ansiyellow">                 self.locals)
</span><span class="ansigreen">    390</span> <span class="ansiyellow"></span>
<span class="ansigreen">    391</span>         with self.fallback_context(';Function "%s" has invalid return type';

<span class="ansigreen">/home/juanlu/.miniconda3/envs/py34/lib/python3.4/site-packages/numba/compiler.py</span> in <span class="ansicyan">type_inference_stage</span><span class="ansiblue">(typingctx, interp, args, return_type, locals)</span>
<span class="ansigreen">    663</span> <span class="ansiyellow"></span>
<span class="ansigreen">    664</span>     infer<span class="ansiyellow">.</span>build_constrain<span class="ansiyellow">(</span><span class="ansiyellow">)</span><span class="ansiyellow"></span>
<span class="ansigreen">--&gt; 665</span><span class="ansiyellow">     </span>infer<span class="ansiyellow">.</span>propagate<span class="ansiyellow">(</span><span class="ansiyellow">)</span><span class="ansiyellow"></span>
<span class="ansigreen">    666</span>     typemap<span class="ansiyellow">,</span> restype<span class="ansiyellow">,</span> calltypes <span class="ansiyellow">=</span> infer<span class="ansiyellow">.</span>unify<span class="ansiyellow">(</span><span class="ansiyellow">)</span><span class="ansiyellow"></span>
<span class="ansigreen">    667</span> <span class="ansiyellow"></span>

<span class="ansigreen">/home/juanlu/.miniconda3/envs/py34/lib/python3.4/site-packages/numba/typeinfer.py</span> in <span class="ansicyan">propagate</span><span class="ansiblue">(self)</span>
<span class="ansigreen">    388</span>                 print<span class="ansiyellow">(</span><span class="ansiblue">"propagate"</span><span class="ansiyellow">.</span>center<span class="ansiyellow">(</span><span class="ansicyan">80</span><span class="ansiyellow">,</span> <span class="ansiblue">';-';</span><span class="ansiyellow">)</span><span class="ansiyellow">)</span><span class="ansiyellow"></span>
<span class="ansigreen">    389</span>             oldtoken <span class="ansiyellow">=</span> newtoken<span class="ansiyellow"></span>
<span class="ansigreen">--&gt; 390</span><span class="ansiyellow">             </span>self<span class="ansiyellow">.</span>constrains<span class="ansiyellow">.</span>propagate<span class="ansiyellow">(</span>self<span class="ansiyellow">.</span>context<span class="ansiyellow">,</span> self<span class="ansiyellow">.</span>typevars<span class="ansiyellow">)</span><span class="ansiyellow"></span>
<span class="ansigreen">    391</span>             newtoken <span class="ansiyellow">=</span> self<span class="ansiyellow">.</span>get_state_token<span class="ansiyellow">(</span><span class="ansiyellow">)</span><span class="ansiyellow"></span>
<span class="ansigreen">    392</span>             <span class="ansigreen">if</span> config<span class="ansiyellow">.</span>DEBUG<span class="ansiyellow">:</span><span class="ansiyellow"></span>

<span class="ansigreen">/home/juanlu/.miniconda3/envs/py34/lib/python3.4/site-packages/numba/typeinfer.py</span> in <span class="ansicyan">propagate</span><span class="ansiblue">(self, context, typevars)</span>
<span class="ansigreen">    110</span>         <span class="ansigreen">for</span> constrain <span class="ansigreen">in</span> self<span class="ansiyellow">.</span>constrains<span class="ansiyellow">:</span><span class="ansiyellow"></span>
<span class="ansigreen">    111</span>             <span class="ansigreen">try</span><span class="ansiyellow">:</span><span class="ansiyellow"></span>
<span class="ansigreen">--&gt; 112</span><span class="ansiyellow">                 </span>constrain<span class="ansiyellow">(</span>context<span class="ansiyellow">,</span> typevars<span class="ansiyellow">)</span><span class="ansiyellow"></span>
<span class="ansigreen">    113</span>             <span class="ansigreen">except</span> TypingError<span class="ansiyellow">:</span><span class="ansiyellow"></span>
<span class="ansigreen">    114</span>                 <span class="ansigreen">raise</span><span class="ansiyellow"></span>

<span class="ansigreen">/home/juanlu/.miniconda3/envs/py34/lib/python3.4/site-packages/numba/typeinfer.py</span> in <span class="ansicyan">__call__</span><span class="ansiblue">(self, context, typevars)</span>
<span class="ansigreen">    267</span>         <span class="ansigreen">for</span> ty <span class="ansigreen">in</span> valtys<span class="ansiyellow">:</span><span class="ansiyellow"></span>
<span class="ansigreen">    268</span>             <span class="ansigreen">try</span><span class="ansiyellow">:</span><span class="ansiyellow"></span>
<span class="ansigreen">--&gt; 269</span><span class="ansiyellow">                 </span>attrty <span class="ansiyellow">=</span> context<span class="ansiyellow">.</span>resolve_getattr<span class="ansiyellow">(</span>value<span class="ansiyellow">=</span>ty<span class="ansiyellow">,</span> attr<span class="ansiyellow">=</span>self<span class="ansiyellow">.</span>attr<span class="ansiyellow">)</span><span class="ansiyellow"></span>
<span class="ansigreen">    270</span>             <span class="ansigreen">except</span> KeyError<span class="ansiyellow">:</span><span class="ansiyellow"></span>
<span class="ansigreen">    271</span>                 args <span class="ansiyellow">=</span> <span class="ansiyellow">(</span>self<span class="ansiyellow">.</span>attr<span class="ansiyellow">,</span> ty<span class="ansiyellow">,</span> self<span class="ansiyellow">.</span>value<span class="ansiyellow">.</span>name<span class="ansiyellow">,</span> self<span class="ansiyellow">.</span>inst<span class="ansiyellow">)</span><span class="ansiyellow"></span>

<span class="ansigreen">/home/juanlu/.miniconda3/envs/py34/lib/python3.4/site-packages/numba/typing/context.py</span> in <span class="ansicyan">resolve_getattr</span><span class="ansiblue">(self, value, attr)</span>
<span class="ansigreen">     82</span>                 <span class="ansigreen">raise</span><span class="ansiyellow"></span>
<span class="ansigreen">     83</span> <span class="ansiyellow"></span>
<span class="ansigreen">---&gt; 84</span><span class="ansiyellow">         </span>ret <span class="ansiyellow">=</span> attrinfo<span class="ansiyellow">.</span>resolve<span class="ansiyellow">(</span>value<span class="ansiyellow">,</span> attr<span class="ansiyellow">)</span><span class="ansiyellow"></span>
<span class="ansigreen">     85</span>         <span class="ansigreen">assert</span> ret<span class="ansiyellow"></span>
<span class="ansigreen">     86</span>         <span class="ansigreen">return</span> ret<span class="ansiyellow"></span>

<span class="ansigreen">/home/juanlu/.miniconda3/envs/py34/lib/python3.4/site-packages/numba/typing/templates.py</span> in <span class="ansicyan">resolve</span><span class="ansiblue">(self, value, attr)</span>
<span class="ansigreen">    241</span>         ret <span class="ansiyellow">=</span> self<span class="ansiyellow">.</span>_resolve<span class="ansiyellow">(</span>value<span class="ansiyellow">,</span> attr<span class="ansiyellow">)</span><span class="ansiyellow"></span>
<span class="ansigreen">    242</span>         <span class="ansigreen">if</span> ret <span class="ansigreen">is</span> <span class="ansigreen">None</span><span class="ansiyellow">:</span><span class="ansiyellow"></span>
<span class="ansigreen">--&gt; 243</span><span class="ansiyellow">             </span><span class="ansigreen">raise</span> UntypedAttributeError<span class="ansiyellow">(</span>value<span class="ansiyellow">=</span>value<span class="ansiyellow">,</span> attr<span class="ansiyellow">=</span>attr<span class="ansiyellow">)</span><span class="ansiyellow"></span>
<span class="ansigreen">    244</span>         <span class="ansigreen">return</span> ret<span class="ansiyellow"></span>
<span class="ansigreen">    245</span> <span class="ansiyellow"></span>

<span class="ansired">UntypedAttributeError</span>: Failed at nopython (nopython frontend)
Unknown attribute "zeros_like" of type Module(&lt;module ';numpy'; from ';/home/juanlu/.miniconda3/envs/py34/lib/python3.4/site-packages/numpy/__init__.py';&gt;)</pre>
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
      Me dice que no conoce la función <code>zeros_like</code>. Si acudimos a la documentación, podemos ver las <a href="http://numba.pydata.org/numba-doc/0.17.0/reference/numpysupported.html">características de NumPy soportadas por numba</a> y las funciones de creación de arrays <em>no</em> figuran entre ellas. Esto es consistente con lo que hemos dicho más arriba: no vamos a poder asignar memoria a objetos nuevos.</p>
    </div>
  </div>
</div>

<div>
  <div>
  </div>
  
  <div>
    <div>
      <h3 id="Paso-3:-Reestructurar-el-c&#243;digo">
        Paso 3: Reestructurar el c&#243;digo<a class="anchor-link" href="-Reestructurar-el-c&#243;digo">&#182;</a>
      </h3>
      
      <p>
        ¿Estamos en un callejón sin salida entonces? ¡En absoluto! Lo que vamos a hacer va a ser separar la parte intensiva de la función para aplicar <code>numba.jit</code> sobre ella, e inicializar todos los valores desde fuera. Para los que hayan usado subrutinas en Fortran este enfoque les resultará familiar 🙂
      </p>
    </div>
  </div>
</div>

<div>
  <div>
    <div>
      <div>
        <div class=" highlight hl-ipython3">
          <pre><span class="k">def</span> <span class="nf">busca_min_np_jit</span><span class="p">(</span><span class="n">malla</span><span class="p">):</span>
    <span class="n">minimos</span> <span class="o">=</span> <span class="n">np</span><span class="o">.</span><span class="n">zeros_like</span><span class="p">(</span><span class="n">malla</span><span class="p">,</span> <span class="n">dtype</span><span class="o">=</span><span class="nb">bool</span><span class="p">)</span>

    <span class="n">_busca_min</span><span class="p">(</span><span class="n">malla</span><span class="p">,</span> <span class="n">minimos</span><span class="p">)</span>

    <span class="k">return</span> <span class="n">np</span><span class="o">.</span><span class="n">nonzero</span><span class="p">(</span><span class="n">minimos</span><span class="p">)</span>

<span class="nd">@numba</span><span class="o">.</span><span class="n">jit</span><span class="p">(</span><span class="n">nopython</span><span class="o">=</span><span class="k">True</span><span class="p">)</span>
<span class="k">def</span> <span class="nf">_busca_min</span><span class="p">(</span><span class="n">malla</span><span class="p">,</span> <span class="n">minimos</span><span class="p">):</span>
    <span class="k">for</span> <span class="n">i</span> <span class="ow">in</span> <span class="nb">range</span><span class="p">(</span><span class="mi">1</span><span class="p">,</span> <span class="n">malla</span><span class="o">.</span><span class="n">shape</span><span class="p">[</span><span class="mi">1</span><span class="p">]</span><span class="o">-</span><span class="mi">1</span><span class="p">):</span>
        <span class="k">for</span> <span class="n">j</span> <span class="ow">in</span> <span class="nb">range</span><span class="p">(</span><span class="mi">1</span><span class="p">,</span> <span class="n">malla</span><span class="o">.</span><span class="n">shape</span><span class="p">[</span><span class="mi"></span><span class="p">]</span><span class="o">-</span><span class="mi">1</span><span class="p">):</span>
            <span class="k">if</span> <span class="p">(</span><span class="n">malla</span><span class="p">[</span><span class="n">j</span><span class="p">,</span> <span class="n">i</span><span class="p">]</span> <span class="o">&lt;</span> <span class="n">malla</span><span class="p">[</span><span class="n">j</span><span class="o">-</span><span class="mi">1</span><span class="p">,</span> <span class="n">i</span><span class="o">-</span><span class="mi">1</span><span class="p">]</span> <span class="ow">and</span>
                <span class="n">malla</span><span class="p">[</span><span class="n">j</span><span class="p">,</span> <span class="n">i</span><span class="p">]</span> <span class="o">&lt;</span> <span class="n">malla</span><span class="p">[</span><span class="n">j</span><span class="o">-</span><span class="mi">1</span><span class="p">,</span> <span class="n">i</span><span class="p">]</span> <span class="ow">and</span>
                <span class="n">malla</span><span class="p">[</span><span class="n">j</span><span class="p">,</span> <span class="n">i</span><span class="p">]</span> <span class="o">&lt;</span> <span class="n">malla</span><span class="p">[</span><span class="n">j</span><span class="o">-</span><span class="mi">1</span><span class="p">,</span> <span class="n">i</span><span class="o">+</span><span class="mi">1</span><span class="p">]</span> <span class="ow">and</span>
                <span class="n">malla</span><span class="p">[</span><span class="n">j</span><span class="p">,</span> <span class="n">i</span><span class="p">]</span> <span class="o">&lt;</span> <span class="n">malla</span><span class="p">[</span><span class="n">j</span><span class="p">,</span> <span class="n">i</span><span class="o">-</span><span class="mi">1</span><span class="p">]</span> <span class="ow">and</span>
                <span class="n">malla</span><span class="p">[</span><span class="n">j</span><span class="p">,</span> <span class="n">i</span><span class="p">]</span> <span class="o">&lt;</span> <span class="n">malla</span><span class="p">[</span><span class="n">j</span><span class="p">,</span> <span class="n">i</span><span class="o">+</span><span class="mi">1</span><span class="p">]</span> <span class="ow">and</span>
                <span class="n">malla</span><span class="p">[</span><span class="n">j</span><span class="p">,</span> <span class="n">i</span><span class="p">]</span> <span class="o">&lt;</span> <span class="n">malla</span><span class="p">[</span><span class="n">j</span><span class="o">+</span><span class="mi">1</span><span class="p">,</span> <span class="n">i</span><span class="o">-</span><span class="mi">1</span><span class="p">]</span> <span class="ow">and</span>
                <span class="n">malla</span><span class="p">[</span><span class="n">j</span><span class="p">,</span> <span class="n">i</span><span class="p">]</span> <span class="o">&lt;</span> <span class="n">malla</span><span class="p">[</span><span class="n">j</span><span class="o">+</span><span class="mi">1</span><span class="p">,</span> <span class="n">i</span><span class="p">]</span> <span class="ow">and</span>
                <span class="n">malla</span><span class="p">[</span><span class="n">j</span><span class="p">,</span> <span class="n">i</span><span class="p">]</span> <span class="o">&lt;</span> <span class="n">malla</span><span class="p">[</span><span class="n">j</span><span class="o">+</span><span class="mi">1</span><span class="p">,</span> <span class="n">i</span><span class="o">+</span><span class="mi">1</span><span class="p">]):</span>
                <span class="n">minimos</span><span class="p">[</span><span class="n">i</span><span class="p">,</span> <span class="n">j</span><span class="p">]</span> <span class="o">=</span> <span class="k">True</span>
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
      Veamos qué ocurre ahora:</p>
    </div>
  </div>
</div>

<div>
  <div>
    <div>
      <div>
        <div class=" highlight hl-ipython3">
          <pre><span class="n">busca_min_np_jit</span><span class="p">(</span><span class="n">data</span><span class="p">)</span>
</pre>
        </div>
      </div>
    </div>
  </div>
  
  <div>
    <div>
      <div>
        <div>
        </div>
        
        <div>
          <pre>(array([   1,    1,    1, ..., 1998, 1998, 1998]),
 array([   1,    3,   11, ..., 1968, 1977, 1985]))</pre>
        </div>
      </div>
    </div>
  </div>
</div>

<div>
  <div>
    <div>
      <div>
        <div class=" highlight hl-ipython3">
          <pre><span class="n">np</span><span class="o">.</span><span class="n">testing</span><span class="o">.</span><span class="n">assert_array_equal</span><span class="p">(</span><span class="n">busca_min</span><span class="p">(</span><span class="n">data</span><span class="p">)[</span><span class="mi"></span><span class="p">],</span> <span class="n">busca_min_np_jit</span><span class="p">(</span><span class="n">data</span><span class="p">)[</span><span class="mi"></span><span class="p">])</span>
<span class="n">np</span><span class="o">.</span><span class="n">testing</span><span class="o">.</span><span class="n">assert_array_equal</span><span class="p">(</span><span class="n">busca_min</span><span class="p">(</span><span class="n">data</span><span class="p">)[</span><span class="mi">1</span><span class="p">],</span> <span class="n">busca_min_np_jit</span><span class="p">(</span><span class="n">data</span><span class="p">)[</span><span class="mi">1</span><span class="p">])</span>
</pre>
        </div>
      </div>
    </div>
  </div>
</div>

<div>
  <div>
    <div>
      <div>
        <div class=" highlight hl-ipython3">
          <pre><span class="o">%</span><span class="k">timeit</span> busca_min_np_jit(data)
</pre>
        </div>
      </div>
    </div>
  </div>
  
  <div>
    <div>
      <div>
        <div>
        </div>
        
        <div>
          <pre>10 loops, best of 3: 62.9 ms per loop
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
      Habéis leído bien: <strong>70x más rápido</strong> 🙂<br /> ¡Lo hemos conseguido! Ahora nuestro código funciona en numba sin problemas y encima es endemoniadamente rápido. Para completar la comparación en mi ordenador, voy a reproducir también la función hecha en Cython:</p>
    </div>
  </div>
</div>

<div>
  <div>
    <div>
      <div>
        <div class=" highlight hl-ipython3">
          <pre><span class="o">%</span><span class="k">load_ext</span> cython
</pre>
        </div>
      </div>
    </div>
  </div>
</div>

<div>
  <div>
    <div>
      <div>
        <div class=" highlight hl-ipython3">
          <pre><span class="o">%%</span><span class="n">cython</span> <span class="o">--</span><span class="n">name</span> <span class="n">probandocython9</span>
<span class="k">import</span> <span class="nn">numpy</span> <span class="k">as</span> <span class="nn">np</span>
<span class="k">cimport</span> <span class="nn">numpy</span> <span class="k">as</span> <span class="nn">np</span>
<span class="k">from</span> <span class="nn">cpython</span> <span class="k">cimport</span> <span class="n">array</span> <span class="k">as</span> <span class="n">c_array</span>
<span class="k">from</span> <span class="nn">array</span> <span class="k">import</span> <span class="n">array</span>
<span class="k">cimport</span> <span class="nn">cython</span>

<span class="nd">@cython</span><span class="o">.</span><span class="n">boundscheck</span><span class="p">(</span><span class="bp">False</span><span class="p">)</span> 
<span class="nd">@cython</span><span class="o">.</span><span class="n">wraparound</span><span class="p">(</span><span class="bp">False</span><span class="p">)</span>
<span class="k">cpdef</span> <span class="kt">tuple</span> <span class="nf">busca_min_cython9</span><span class="p">(</span><span class="n">double</span> <span class="p">[:,:]</span> <span class="n">malla</span><span class="p">):</span>
    <span class="k">cdef</span> <span class="kt">c_array</span>.<span class="kt">array</span> <span class="nf">minimosx</span><span class="p">,</span> <span class="nf">minimosy</span>
    <span class="k">cdef</span> <span class="kt">unsigned</span> <span class="kt">int</span> <span class="nf">i</span><span class="p">,</span> <span class="nf">j</span>
    <span class="k">cdef</span> <span class="kt">unsigned</span> <span class="kt">int</span> <span class="nf">ii</span> <span class="o">=</span> <span class="n">malla</span><span class="o">.</span><span class="n">shape</span><span class="p">[</span><span class="mf">1</span><span class="p">]</span><span class="o">-</span><span class="mf">1</span>
    <span class="k">cdef</span> <span class="kt">unsigned</span> <span class="kt">int</span> <span class="nf">jj</span> <span class="o">=</span> <span class="n">malla</span><span class="o">.</span><span class="n">shape</span><span class="p">[</span><span class="mf"></span><span class="p">]</span><span class="o">-</span><span class="mf">1</span>
    <span class="k">cdef</span> <span class="kt">unsigned</span> <span class="kt">int</span> <span class="nf">start</span> <span class="o">=</span> <span class="mf">1</span>
    <span class="c">#cdef float [:, :] malla_view = malla</span>
    <span class="n">minimosx</span> <span class="o">=</span> <span class="n">array</span><span class="p">(</span><span class="s">&#039;L&#039;</span><span class="p">,</span> <span class="p">[])</span>
    <span class="n">minimosy</span> <span class="o">=</span> <span class="n">array</span><span class="p">(</span><span class="s">&#039;L&#039;</span><span class="p">,</span> <span class="p">[])</span> 
    <span class="k">for</span> <span class="n">i</span> <span class="ow">in</span> <span class="nb">range</span><span class="p">(</span><span class="n">start</span><span class="p">,</span> <span class="n">ii</span><span class="p">):</span>
        <span class="k">for</span> <span class="n">j</span> <span class="ow">in</span> <span class="nb">range</span><span class="p">(</span><span class="n">start</span><span class="p">,</span> <span class="n">jj</span><span class="p">):</span>
            <span class="k">if</span> <span class="p">(</span><span class="n">malla</span><span class="p">[</span><span class="n">j</span><span class="p">,</span> <span class="n">i</span><span class="p">]</span> <span class="o">&lt;</span> <span class="n">malla</span><span class="p">[</span><span class="n">j</span><span class="o">-</span><span class="mf">1</span><span class="p">,</span> <span class="n">i</span><span class="o">-</span><span class="mf">1</span><span class="p">]</span> <span class="ow">and</span>
                <span class="n">malla</span><span class="p">[</span><span class="n">j</span><span class="p">,</span> <span class="n">i</span><span class="p">]</span> <span class="o">&lt;</span> <span class="n">malla</span><span class="p">[</span><span class="n">j</span><span class="o">-</span><span class="mf">1</span><span class="p">,</span> <span class="n">i</span><span class="p">]</span> <span class="ow">and</span>
                <span class="n">malla</span><span class="p">[</span><span class="n">j</span><span class="p">,</span> <span class="n">i</span><span class="p">]</span> <span class="o">&lt;</span> <span class="n">malla</span><span class="p">[</span><span class="n">j</span><span class="o">-</span><span class="mf">1</span><span class="p">,</span> <span class="n">i</span><span class="o">+</span><span class="mf">1</span><span class="p">]</span> <span class="ow">and</span>
                <span class="n">malla</span><span class="p">[</span><span class="n">j</span><span class="p">,</span> <span class="n">i</span><span class="p">]</span> <span class="o">&lt;</span> <span class="n">malla</span><span class="p">[</span><span class="n">j</span><span class="p">,</span> <span class="n">i</span><span class="o">-</span><span class="mf">1</span><span class="p">]</span> <span class="ow">and</span>
                <span class="n">malla</span><span class="p">[</span><span class="n">j</span><span class="p">,</span> <span class="n">i</span><span class="p">]</span> <span class="o">&lt;</span> <span class="n">malla</span><span class="p">[</span><span class="n">j</span><span class="p">,</span> <span class="n">i</span><span class="o">+</span><span class="mf">1</span><span class="p">]</span> <span class="ow">and</span>
                <span class="n">malla</span><span class="p">[</span><span class="n">j</span><span class="p">,</span> <span class="n">i</span><span class="p">]</span> <span class="o">&lt;</span> <span class="n">malla</span><span class="p">[</span><span class="n">j</span><span class="o">+</span><span class="mf">1</span><span class="p">,</span> <span class="n">i</span><span class="o">-</span><span class="mf">1</span><span class="p">]</span> <span class="ow">and</span>
                <span class="n">malla</span><span class="p">[</span><span class="n">j</span><span class="p">,</span> <span class="n">i</span><span class="p">]</span> <span class="o">&lt;</span> <span class="n">malla</span><span class="p">[</span><span class="n">j</span><span class="o">+</span><span class="mf">1</span><span class="p">,</span> <span class="n">i</span><span class="p">]</span> <span class="ow">and</span>
                <span class="n">malla</span><span class="p">[</span><span class="n">j</span><span class="p">,</span> <span class="n">i</span><span class="p">]</span> <span class="o">&lt;</span> <span class="n">malla</span><span class="p">[</span><span class="n">j</span><span class="o">+</span><span class="mf">1</span><span class="p">,</span> <span class="n">i</span><span class="o">+</span><span class="mf">1</span><span class="p">]):</span>
                <span class="n">minimosx</span><span class="o">.</span><span class="n">append</span><span class="p">(</span><span class="n">i</span><span class="p">)</span>
                <span class="n">minimosy</span><span class="o">.</span><span class="n">append</span><span class="p">(</span><span class="n">j</span><span class="p">)</span>

    <span class="k">return</span> <span class="n">np</span><span class="o">.</span><span class="n">array</span><span class="p">(</span><span class="n">minimosx</span><span class="p">),</span> <span class="n">np</span><span class="o">.</span><span class="n">array</span><span class="p">(</span><span class="n">minimosy</span><span class="p">)</span>
</pre>
        </div>
      </div>
    </div>
  </div>
</div>

<div>
  <div>
    <div>
      <div>
        <div class=" highlight hl-ipython3">
          <pre><span class="o">%</span><span class="k">timeit</span> busca_min_cython9(data)
</pre>
        </div>
      </div>
    </div>
  </div>
  
  <div>
    <div>
      <div>
        <div>
        </div>
        
        <div>
          <pre>10 loops, best of 3: 151 ms per loop
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
      Por tanto, vemos que <strong>la versión con numba es el doble de rápida que la versión con Cython</strong>. Sobre gustos no hay nada escrito: yo por ejemplo valoro no «salirme» de Python usando numba mientras que a otro puede no importarle incluir especificaciones de tipos como en Cython. Los números, eso sí, son los números 🙂</p>
    </div>
  </div>
</div>

<div>
  <div>
  </div>
  
  <div>
    <div>
      <h2 id="M&#225;s-casos-de-&#233;xito">
        M&#225;s casos de &#233;xito<a class="anchor-link" href="#M&#225;s-casos-de-&#233;xito">&#182;</a>
      </h2>
    </div>
  </div>
</div>

<div>
  <div>
  </div>
  
  <div>
    <div>
      <h3 id="La-atm&#243;sfera-est&#225;ndar">
        La atm&#243;sfera est&#225;ndar<a class="anchor-link" href="#La-atm&#243;sfera-est&#225;ndar">&#182;</a>
      </h3>
      
      <p>
        El <strong>cálculo de propiedades termodinámicas de la atmósfera estándar</strong> es un problema clásico que todo aeronáutico ha afrontado alguna vez muy al principio de su carrera formativa. La teoría es simple: imponemos una ley de variación de la temperatura con la altura $T = T(h)$, la presión se obtiene por consideraciones hidrostáticas $p = p(T)$ y la densidad por la ecuación de los gases ideales $\rho = \rho(p, T)$. La particularidad de la atmósfera estándar es que imponemos que la variación de la temperatura con la altura es una función simplificada <em>y definida a trozos</em>, así que calcular temperatura, presión y densidad dada una altura se parece mucho a hacer esto:
      </p>
    </div>
  </div>
</div>

<div>
  <div>
    <div>
      <div>
        <div class=" highlight hl-ipython3">
          <pre><span class="k">if</span> <span class="mf">0.0</span> <span class="o">&lt;=</span> <span class="n">h</span> <span class="o">&lt;</span> <span class="mf">11000.0</span><span class="p">:</span>
    <span class="n">T</span> <span class="o">=</span> <span class="n">T0</span> <span class="o">+</span> <span class="n">alpha</span> <span class="o">*</span> <span class="n">h</span>
    <span class="n">p</span> <span class="o">=</span> <span class="o">...</span>  <span class="c"># Algo que depende de T</span>
    <span class="n">rho</span> <span class="o">=</span> <span class="n">p</span> <span class="o">/</span> <span class="p">(</span><span class="n">R_a</span> <span class="o">*</span> <span class="n">T</span><span class="p">)</span>
<span class="k">elif</span> <span class="mf">11000.0</span> <span class="o">&lt;=</span> <span class="n">h</span> <span class="o">&lt;</span> <span class="mf">20000.0</span><span class="p">:</span>
    <span class="n">T</span> <span class="o">=</span> <span class="n">T1</span>
    <span class="n">p</span> <span class="o">=</span> <span class="o">...</span>
    <span class="n">rho</span> <span class="o">=</span> <span class="n">p</span> <span class="o">/</span> <span class="p">(</span><span class="n">R_a</span> <span class="o">*</span> <span class="n">T</span><span class="p">)</span>
<span class="k">elif</span> <span class="mf">20000.0</span> <span class="o">&lt;=</span> <span class="n">h</span> <span class="o">&lt;=</span> <span class="mf">32000.0</span><span class="p">:</span>
    <span class="o">...</span>
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
      El problema viene cuando se quiere <strong>vectorizar</strong> esta función y permitir que <code>h</code> pueda ser un array de alturas. Esto es muy conveniente cuando queremos pintar alguna propiedad con matplotlib, por ejemplo.<br /> Se intuye que hay dos formas de hacer esto: utilizando funciones de NumPy o iterando por cada elemento del array. La primera solución se hace farragosa, y la segunda, gracias a la proverbial lentitud de Python, es extremadamente lenta. Mi amigo <a href="http://twitter.com/Alex__S12">Álex</a> y yo llevamos pensando sobre este problema <em>años</em>, y nunca hemos llegado a una solución satisfactoria (incluso <a href="https://github.com/numpy/numpy/pull/331">encontramos algunos bugs en <code>numpy.piecewise</code></a> por el camino). Este año decidimos cerrar este asunto definitivamente así que con <a href="https://github.com/AeroPython">el equipo AeroPython</a> exploramos varias implementaciones distintas. Hasta que por fin lo conseguimos: <strong>usamos numba para acelerar los bucles</strong>.<br /> <img src="https://cloud.githubusercontent.com/assets/316517/6236738/63dabc48-b6ed-11e4-822f-2c36c0d96f76.png" alt="numba gana a C++" /><br /> Como podéis leer <a href="https://github.com/AeroPython/aeropy/issues/4#issuecomment-74748524">en la discusión original</a>, la función de la primera columna está escrita en C++. ¿Impresionado? 😉</p>
    </div>
  </div>
</div>

<div>
  <div>
  </div>
  
  <div>
    <div>
      <h3 id="Soluci&#243;n-de-Navier-de-una-placa-plana">
        Soluci&#243;n de Navier de una placa plana<a class="anchor-link" href="#Soluci&#243;n-de-Navier-de-una-placa-plana">&#182;</a>
      </h3>
      
      <p>
        Para mi proyecto fin de carrera me encontré con la necesidad de calcular la deflexión de una placa rectangular, simplemente apoyada en sus cuatro bordes (es decir, los bordes pueden girar: no están empotrados) sometida a una carga transversal. Este problema tiene solución analítica conocida desde hace tiempo, hallada por Navier:<br /> $\displaystyle w(x,y) = \sum_{m=1}^\infty \sum_{n=1}^\infty \frac{a_{mn}}{\pi^4 D}\,\left(\frac{m^2}{a^2}+\frac{n^2}{b^2}\right)^{-2}\,\sin\frac{m \pi x}{a}\sin\frac{n \pi y}{b}$
      </p>
      
      <p>
        siendo $a_{mn}$ los coeficientes de Fourier de la carga aplicada. Como veis, para cada punto $(x, y)$ hay que hacer una doble suma en serie; si encima queremos evaluar esto en un <code>meshgrid</code>, necesitamos <strong>un cuádruple bucle</strong>. Ya se anticipa que por muy hábiles que estemos, a Python le va a costar.<br /> La clave estuvo, una vez más, en usar numba para optimizar los bucles. En GitHub tenéis <a href="https://gist.github.com/Juanlu001/cf19b1c16caf618860fb">el código completo</a>, pero la parte importante es esta:
      </p>
    </div>
  </div>
</div>

<div>
  <div>
    <div>
      <div>
        <div class=" highlight hl-ipython3">
          <pre><span class="nd">@numba</span><span class="o">.</span><span class="n">jit</span><span class="p">(</span><span class="n">nopython</span><span class="o">=</span><span class="k">True</span><span class="p">)</span>
<span class="k">def</span> <span class="nf">a_mn_point</span><span class="p">(</span><span class="n">P</span><span class="p">,</span> <span class="n">a</span><span class="p">,</span> <span class="n">b</span><span class="p">,</span> <span class="n">xi</span><span class="p">,</span> <span class="n">eta</span><span class="p">,</span> <span class="n">mm</span><span class="p">,</span> <span class="n">nn</span><span class="p">):</span>
    <span class="sd">"""Navier series coefficient for concentrated load.</span>

<span class="sd">    """</span>
    <span class="k">return</span> <span class="mi">4</span> <span class="o">*</span> <span class="n">P</span> <span class="o">*</span> <span class="n">sin</span><span class="p">(</span><span class="n">mm</span> <span class="o">*</span> <span class="n">pi</span> <span class="o">*</span> <span class="n">xi</span> <span class="o">/</span> <span class="n">a</span><span class="p">)</span> <span class="o">*</span> <span class="n">sin</span><span class="p">(</span><span class="n">nn</span> <span class="o">*</span> <span class="n">pi</span> <span class="o">*</span> <span class="n">eta</span> <span class="o">/</span> <span class="n">b</span><span class="p">)</span> <span class="o">/</span> <span class="p">(</span><span class="n">a</span> <span class="o">*</span> <span class="n">b</span><span class="p">)</span>
 
 
<span class="nd">@numba</span><span class="o">.</span><span class="n">jit</span><span class="p">(</span><span class="n">nopython</span><span class="o">=</span><span class="k">True</span><span class="p">)</span>
<span class="k">def</span> <span class="nf">plate_displacement</span><span class="p">(</span><span class="n">xx</span><span class="p">,</span> <span class="n">yy</span><span class="p">,</span> <span class="n">ww</span><span class="p">,</span> <span class="n">a</span><span class="p">,</span> <span class="n">b</span><span class="p">,</span> <span class="n">P</span><span class="p">,</span> <span class="n">xi</span><span class="p">,</span> <span class="n">eta</span><span class="p">,</span> <span class="n">D</span><span class="p">,</span> <span class="n">max_m</span><span class="p">,</span> <span class="n">max_n</span><span class="p">):</span>
    <span class="n">max_i</span><span class="p">,</span> <span class="n">max_j</span> <span class="o">=</span> <span class="n">ww</span><span class="o">.</span><span class="n">shape</span>
    <span class="k">for</span> <span class="n">mm</span> <span class="ow">in</span> <span class="nb">range</span><span class="p">(</span><span class="mi">1</span><span class="p">,</span> <span class="n">max_m</span><span class="p">):</span>
        <span class="k">for</span> <span class="n">nn</span> <span class="ow">in</span> <span class="nb">range</span><span class="p">(</span><span class="mi">1</span><span class="p">,</span> <span class="n">max_n</span><span class="p">):</span>
            <span class="k">for</span> <span class="n">ii</span> <span class="ow">in</span> <span class="nb">range</span><span class="p">(</span><span class="n">max_i</span><span class="p">):</span>
                <span class="k">for</span> <span class="n">jj</span> <span class="ow">in</span> <span class="nb">range</span><span class="p">(</span><span class="n">max_j</span><span class="p">):</span>
                    <span class="n">a_mn</span> <span class="o">=</span> <span class="n">a_mn_point</span><span class="p">(</span><span class="n">P</span><span class="p">,</span> <span class="n">a</span><span class="p">,</span> <span class="n">b</span><span class="p">,</span> <span class="n">xi</span><span class="p">,</span> <span class="n">eta</span><span class="p">,</span> <span class="n">mm</span><span class="p">,</span> <span class="n">nn</span><span class="p">)</span>
                    <span class="n">ww</span><span class="p">[</span><span class="n">ii</span><span class="p">,</span> <span class="n">jj</span><span class="p">]</span> <span class="o">+=</span> <span class="p">(</span><span class="n">a_mn</span> <span class="o">/</span> <span class="p">(</span><span class="n">mm</span><span class="o">**</span><span class="mi">2</span> <span class="o">/</span> <span class="n">a</span><span class="o">**</span><span class="mi">2</span> <span class="o">+</span> <span class="n">nn</span><span class="o">**</span><span class="mi">2</span> <span class="o">/</span> <span class="n">b</span><span class="o">**</span><span class="mi">2</span><span class="p">)</span><span class="o">**</span><span class="mi">2</span>
                                   <span class="o">*</span> <span class="n">sin</span><span class="p">(</span><span class="n">mm</span> <span class="o">*</span> <span class="n">pi</span> <span class="o">*</span> <span class="n">xx</span><span class="p">[</span><span class="n">ii</span><span class="p">,</span> <span class="n">jj</span><span class="p">]</span> <span class="o">/</span> <span class="n">a</span><span class="p">)</span>
                                   <span class="o">*</span> <span class="n">sin</span><span class="p">(</span><span class="n">nn</span> <span class="o">*</span> <span class="n">pi</span> <span class="o">*</span> <span class="n">yy</span><span class="p">[</span><span class="n">ii</span><span class="p">,</span> <span class="n">jj</span><span class="p">]</span> <span class="o">/</span> <span class="n">b</span><span class="p">)</span>
                                   <span class="o">/</span> <span class="p">(</span><span class="n">pi</span><span class="o">**</span><span class="mi">4</span> <span class="o">*</span> <span class="n">D</span><span class="p">))</span> 
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
      <img src="https://camo.githubusercontent.com/9e60d6258ba6e0270338a8afe310db410baacfd0/68747470733a2f2f7062732e7477696d672e636f6d2f6d656469612f4235696459656843454145533470452e706e67" alt="Solución de una placa plana" /></p>
    </div>
  </div>
</div>

<div>
  <div>
  </div>
  
  <div>
    <div>
      Podéis comprobar vosotros mismos que las diferencias de rendimiento en este caso son brutales. <em>Y solo hemos añadido una línea a cada función</em>.</p>
    </div>
  </div>
</div>

<div>
  <div>
  </div>
  
  <div>
    <div>
      <h2 id="Conclusiones">
        Conclusiones<a class="anchor-link" href="#Conclusiones">&#182;</a>
      </h2>
      
      <p>
        numba aún no es una herramienta estable, pero está rápidamente alcanzando un grado de madurez suficiente para optimizar código orientado a operar con arrays. Gracias a conda es trivial de instalar y los resultados respecto a soluciones más maduras como Cython son aplastantes, tanto en velocidad de ejecución como en la complejidad del código resultante.<br /> De momento yo me quedo con numba, ¿y tú? 😉
      </p>
    </div>
  </div>
</div>