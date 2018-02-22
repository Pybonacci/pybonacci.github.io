---
title: Trabajando con Python y R
date: 2015-06-18T19:26:25+00:00
author: Kiko Correoso
slug: trabajando-con-python-y-r
tags: cran, EVA, EVT, extremes, extremos, ipython, R, rpy2

<div>
  <div>
  </div>
  
  <div>
    <div>
      <h1 id="Trabajando-de-forma-conjunta-con-Python-y-con-R.">
        Trabajando de forma conjunta con Python y con R.<a class="anchor-link" href="#Trabajando-de-forma-conjunta-con-Python-y-con-R.">&#182;</a>
      </h1>
    </div>
  </div>
</div>

<div>
  <div>
  </div>
  
  <div>
    <div>
      Hoy vamos a ver como podemos juntar lo bueno de <a href="http://cran.r-project.org/">R</a>, algunas de sus librerías, con Python usando <strong>rpy2</strong>.</p> 
      
      <p>
        Pero, lo primero de todo, ¿<a href="http://rpy.sourceforge.net/">qué es rpy2</a>? rpy2 es una interfaz que permite que podamos comunicar información entre R y Python y que podamos acceder a funcionalidad de R desde Python. Por tanto, podemos estar usando Python para todo nuestro análisis y en el caso de que necesitemos alguna librería estadística especializada de R podremos acceder a la misma usando rpy2.
      </p>
    </div>
  </div>
</div>

<div>
  <div>
  </div>
  
  <div>
    <div>
      Para poder usar rpy2 necesitarás tener <a href="http://rpy.sourceforge.net/rpy2/doc-2.5/html/overview.html#requirements">instalado tanto Python (CPython versión >= 2.7.x) como R (versión >=3)</a>, además de las librerías R a las que quieras acceder. <a href="http://continuum.io/conda-for-R">Conda permite realizar todo el proceso de instalación de los intérpretes de Python y R, además de librerías</a>, pero no he trabajado con Conda y R por lo que no puedo aportar mucho más en este aspecto. Supongo que será parecido a lo que hacemos con Conda y Python.</p>
    </div>
  </div>
</div>

<div>
  <div>
  </div>
  
  <div>
    <div>
      Para este microtutorial voy a hacer uso de la librería <strong><a href="http://cran.r-project.org/web/packages/extRemes/index.html">extRemes</a></strong> de R que permite hacer análisis de valores extremos usando varias de las metodologías más comúnmente aceptadas.</p>
    </div>
  </div>
</div>

<div>
  <div>
  </div>
  
  <div>
    <div>
      Como siempre, primero de todo, importaremos la funcionalidad que necesitamos para la ocasión.</p>
    </div>
  </div>
</div>

<div>
  <div>
    <div>
      <div>
        <div class=" highlight hl-ipython3">
          <pre><span class="c"># Importamos pandas y numpy para manejar los datos que pasaremos a R</span>
<span class="kn">import</span> <span class="nn">pandas</span> <span class="k">as</span> <span class="nn">pd</span>
<span class="kn">import</span> <span class="nn">numpy</span> <span class="k">as</span> <span class="nn">np</span>

<span class="c"># Usamos rpy2 para interactuar con R</span>
<span class="kn">import</span> <span class="nn">rpy2.robjects</span> <span class="k">as</span> <span class="nn">ro</span>

<span class="c"># Activamos la conversión automática de tipos de rpy2</span>
<span class="kn">import</span> <span class="nn">rpy2.robjects.numpy2ri</span>
<span class="n">rpy2</span><span class="o">.</span><span class="n">robjects</span><span class="o">.</span><span class="n">numpy2ri</span><span class="o">.</span><span class="n">activate</span><span class="p">()</span>

<span class="kn">import</span> <span class="nn">matplotlib.pyplot</span> <span class="k">as</span> <span class="nn">plt</span>
<span class="o">%</span><span class="k">matplotlib</span> inline
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
      En el anterior código podemos ver una serie de cosas nuevas que voy a explicar brevemente:</p> 
      
      <ul>
        <li>
          <code>import rpy2.robjects as ro</code>, esto lo explicaremos un poquito más abajo.
        </li>
        <li>
          <code>import rpy2.robjects.numpy2ri</code>, importamos el módulo numpy2ri. Este módulo permite que hagamos conversión automática de objetos numpy a objetos rpy2.
        </li>
        <li>
          <code>rpy2.robjects.numpy2ri.activate()</code>, hacemos uso de la función <code>activate</code> que activa la conversión automática de objetos que hemos comentado en la línea anterior.
        </li>
      </ul>
    </div>
  </div>
</div>

<div>
  <div>
  </div>
  
  <div>
    <div>
      <h1 id="Brev&#237;sima-introducci&#243;n-a-algunas-de-las-cosas-m&#225;s-importantes-de-rpy2.">
        Brev&#237;sima introducci&#243;n a algunas de las cosas m&#225;s importantes de rpy2.<a class="anchor-link" href="#Brev&#237;sima-introducci&#243;n-a-algunas-de-las-cosas-m&#225;s-importantes-de-rpy2.">&#182;</a>
      </h1>
    </div>
  </div>
</div>

<div>
  <div>
  </div>
  
  <div>
    <div>
      Para evaluar directamente código R podemos hacerlo usando <code>rpy2.robjects.r</code> con el código R expresado como una cadena (<code>rpy2.robjects</code> lo he importado como <code>ro</code> en este caso, como podéis ver más arriba):</p>
    </div>
  </div>
</div>

<div>
  <div>
    <div>
      <div>
        <div class=" highlight hl-ipython3">
          <pre><span class="n">codigo_r</span> <span class="o">=</span> <span class="s">"""</span>
<span class="s">saluda &lt;- function(cadena) {</span>
<span class="s">  return(paste("Hola, ", cadena))</span>
<span class="s">}</span>
<span class="s">"""</span>
<span class="n">ro</span><span class="o">.</span><span class="n">r</span><span class="p">(</span><span class="n">codigo_r</span><span class="p">)</span>
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
          <pre>&lt;SignatureTranslatedFunction - Python:0x03096490 / R:0x03723E98&gt;</pre>
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
      En la anterior celda hemos creado una función R llamada <code>saluda</code> y que ahora está disponible en el espacio de nombres global de R. Podemos acceder a la misma desde Python de la siguiente forma:</p>
    </div>
  </div>
</div>

<div>
  <div>
    <div>
      <div>
        <div class=" highlight hl-ipython3">
          <pre><span class="n">saluda_py</span> <span class="o">=</span> <span class="n">ro</span><span class="o">.</span><span class="n">globalenv</span><span class="p">[</span><span class="s">&#39;saluda&#39;</span><span class="p">]</span>
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
      Y podemos usarla de la siguiente forma:</p>
    </div>
  </div>
</div>

<div>
  <div>
    <div>
      <div>
        <div class=" highlight hl-ipython3">
          <pre><span class="n">res</span> <span class="o">=</span> <span class="n">saluda_py</span><span class="p">(</span><span class="s">&#39;pepe&#39;</span><span class="p">)</span>
<span class="nb">print</span><span class="p">(</span><span class="n">res</span><span class="p">[</span><span class="mi"></span><span class="p">])</span>
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
          <pre>Hola,  pepe
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
      En la anterior celda véis que para acceder al resultado he tenido que usar <code>res[0]</code>. En realidad, lo que nos devuleve rpy2 es:</p>
    </div>
  </div>
</div>

<div>
  <div>
    <div>
      <div>
        <div class=" highlight hl-ipython3">
          <pre><span class="nb">print</span><span class="p">(</span><span class="nb">type</span><span class="p">(</span><span class="n">res</span><span class="p">))</span>
<span class="nb">print</span><span class="p">(</span><span class="n">res</span><span class="o">.</span><span class="n">shape</span><span class="p">)</span>
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
          <pre>&lt;class ';numpy.ndarray';&gt;
(1,)
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
      En este caso un numpy array con diversa información del objeto rpy2. Como el objeto solo devuelve un string pues el numpy array solo tiene un elemento.</p>
    </div>
  </div>
</div>

<div>
  <div>
  </div>
  
  <div>
    <div>
      Podemos acceder al código R de la función de la siguiente forma:</p>
    </div>
  </div>
</div>

<div>
  <div>
    <div>
      <div>
        <div class=" highlight hl-ipython3">
          <pre><span class="nb">print</span><span class="p">(</span><span class="n">saluda_py</span><span class="o">.</span><span class="n">r_repr</span><span class="p">())</span>
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
          <pre>function (cadena) 
{
    return(paste("Hola, ", cadena))
}
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
      Hemos visto como acceder desde Python a nombres disponibles en el entorno global de R. ¿Cómo podemos hacer para que algo que creemos en Python este accesible en R?</p>
    </div>
  </div>
</div>

<div>
  <div>
    <div>
      <div>
        <div class=" highlight hl-ipython3">
          <pre><span class="n">variable_r_creada_desde_python</span> <span class="o">=</span> <span class="n">ro</span><span class="o">.</span><span class="n">FloatVector</span><span class="p">(</span><span class="n">np</span><span class="o">.</span><span class="n">arange</span><span class="p">(</span><span class="mi">1</span><span class="p">,</span><span class="mi">5</span><span class="p">,</span><span class="mf">0.1</span><span class="p">))</span>
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
      Veamos como es esta <code>variable_r_creada_desde_python</code> dentro de Python</p>
    </div>
  </div>
</div>

<div>
  <div>
    <div>
      <div>
        <div class=" highlight hl-ipython3">
          <pre><span class="n">variable_r_creada_desde_python</span>
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
          <pre>&lt;FloatVector - Python:0x09D5A7B0 / R:0x07FE8900&gt;
[1.000000, 1.100000, 1.200000, ..., 4.700000, 4.800000, 4.900000]</pre>
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
      ¿Y lo que se tendría que ver en R?</p>
    </div>
  </div>
</div>

<div>
  <div>
    <div>
      <div>
        <div class=" highlight hl-ipython3">
          <pre><span class="nb">print</span><span class="p">(</span><span class="n">variable_r_creada_desde_python</span><span class="o">.</span><span class="n">r_repr</span><span class="p">())</span>
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
          <pre>c(1, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2, 2.1, 2.2, 
2.3, 2.4, 2.5, 2.6, 2.7, 2.8, 2.9, 3, 3.1, 3.2, 3.3, 3.4, 3.5, 
3.6, 3.7, 3.8, 3.9, 4, 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7, 4.8, 
4.9)
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
      Pero ahora mismo esa variable no está disponible desde R y no la podríamos usar dentro de código R que permanece en el espacio R (vaya lío, ¿no?)</p>
    </div>
  </div>
</div>

<div>
  <div>
    <div>
      <div>
        <div class=" highlight hl-ipython3">
          <pre><span class="n">ro</span><span class="o">.</span><span class="n">r</span><span class="p">(</span><span class="s">&#39;variable_r_creada_desde_python&#39;</span><span class="p">)</span>
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
<span class="ansired">RRuntimeError</span>                             Traceback (most recent call last)
<span class="ansigreen">&lt;ipython-input-10-524753a78365&gt;</span> in <span class="ansicyan">&lt;module&gt;</span><span class="ansiblue">()</span>
<span class="ansigreen">----&gt; 1</span><span class="ansiyellow"> </span>ro<span class="ansiyellow">.</span>r<span class="ansiyellow">(</span><span class="ansiblue">';variable_r_creada_desde_python';</span><span class="ansiyellow">)</span><span class="ansiyellow"></span>

<span class="ansigreen">d:\users\X003621\AppData\Local\Continuum\Miniconda3\lib\site-packages\rpy2\robjects\__init__.py</span> in <span class="ansicyan">__call__</span><span class="ansiblue">(self, string)</span>
<span class="ansigreen">    251</span>     <span class="ansigreen">def</span> __call__<span class="ansiyellow">(</span>self<span class="ansiyellow">,</span> string<span class="ansiyellow">)</span><span class="ansiyellow">:</span><span class="ansiyellow"></span>
<span class="ansigreen">    252</span>         p <span class="ansiyellow">=</span> rinterface<span class="ansiyellow">.</span>parse<span class="ansiyellow">(</span>string<span class="ansiyellow">)</span><span class="ansiyellow"></span>
<span class="ansigreen">--&gt; 253</span><span class="ansiyellow">         </span>res <span class="ansiyellow">=</span> self<span class="ansiyellow">.</span>eval<span class="ansiyellow">(</span>p<span class="ansiyellow">)</span><span class="ansiyellow"></span>
<span class="ansigreen">    254</span>         <span class="ansigreen">return</span> res<span class="ansiyellow"></span>
<span class="ansigreen">    255</span> <span class="ansiyellow"></span>

<span class="ansigreen">d:\users\X003621\AppData\Local\Continuum\Miniconda3\lib\site-packages\rpy2\robjects\functions.py</span> in <span class="ansicyan">__call__</span><span class="ansiblue">(self, *args, **kwargs)</span>
<span class="ansigreen">    168</span>                 v <span class="ansiyellow">=</span> kwargs<span class="ansiyellow">.</span>pop<span class="ansiyellow">(</span>k<span class="ansiyellow">)</span><span class="ansiyellow"></span>
<span class="ansigreen">    169</span>                 kwargs<span class="ansiyellow">[</span>r_k<span class="ansiyellow">]</span> <span class="ansiyellow">=</span> v<span class="ansiyellow"></span>
<span class="ansigreen">--&gt; 170</span><span class="ansiyellow">         </span><span class="ansigreen">return</span> super<span class="ansiyellow">(</span>SignatureTranslatedFunction<span class="ansiyellow">,</span> self<span class="ansiyellow">)</span><span class="ansiyellow">.</span>__call__<span class="ansiyellow">(</span><span class="ansiyellow">*</span>args<span class="ansiyellow">,</span> <span class="ansiyellow">**</span>kwargs<span class="ansiyellow">)</span><span class="ansiyellow"></span>
<span class="ansigreen">    171</span> <span class="ansiyellow"></span>
<span class="ansigreen">    172</span> pattern_link <span class="ansiyellow">=</span> re<span class="ansiyellow">.</span>compile<span class="ansiyellow">(</span><span class="ansiblue">r';\\link\{(.+?)\}';</span><span class="ansiyellow">)</span><span class="ansiyellow"></span>

<span class="ansigreen">d:\users\X003621\AppData\Local\Continuum\Miniconda3\lib\site-packages\rpy2\robjects\functions.py</span> in <span class="ansicyan">__call__</span><span class="ansiblue">(self, *args, **kwargs)</span>
<span class="ansigreen">     98</span>         <span class="ansigreen">for</span> k<span class="ansiyellow">,</span> v <span class="ansigreen">in</span> kwargs<span class="ansiyellow">.</span>items<span class="ansiyellow">(</span><span class="ansiyellow">)</span><span class="ansiyellow">:</span><span class="ansiyellow"></span>
<span class="ansigreen">     99</span>             new_kwargs<span class="ansiyellow">[</span>k<span class="ansiyellow">]</span> <span class="ansiyellow">=</span> conversion<span class="ansiyellow">.</span>py2ri<span class="ansiyellow">(</span>v<span class="ansiyellow">)</span><span class="ansiyellow"></span>
<span class="ansigreen">--&gt; 100</span><span class="ansiyellow">         </span>res <span class="ansiyellow">=</span> super<span class="ansiyellow">(</span>Function<span class="ansiyellow">,</span> self<span class="ansiyellow">)</span><span class="ansiyellow">.</span>__call__<span class="ansiyellow">(</span><span class="ansiyellow">*</span>new_args<span class="ansiyellow">,</span> <span class="ansiyellow">**</span>new_kwargs<span class="ansiyellow">)</span><span class="ansiyellow"></span>
<span class="ansigreen">    101</span>         res <span class="ansiyellow">=</span> conversion<span class="ansiyellow">.</span>ri2ro<span class="ansiyellow">(</span>res<span class="ansiyellow">)</span><span class="ansiyellow"></span>
<span class="ansigreen">    102</span>         <span class="ansigreen">return</span> res<span class="ansiyellow"></span>

<span class="ansired">RRuntimeError</span>: Error in eval(expr, envir, enclos) : 
  object ';variable_r_creada_desde_python'; not found
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
      Vale, tendremos que hacer que sea accesible desde R de la siguiente forma:</p>
    </div>
  </div>
</div>

<div>
  <div>
    <div>
      <div>
        <div class=" highlight hl-ipython3">
          <pre><span class="n">ro</span><span class="o">.</span><span class="n">globalenv</span><span class="p">[</span><span class="s">"variable_ahora_en_r"</span><span class="p">]</span> <span class="o">=</span> <span class="n">variable_r_creada_desde_python</span>
<span class="nb">print</span><span class="p">(</span><span class="n">ro</span><span class="o">.</span><span class="n">r</span><span class="p">(</span><span class="s">"variable_ahora_en_r"</span><span class="p">))</span>
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
          <pre>[ 1.   1.1  1.2  1.3  1.4  1.5  1.6  1.7  1.8  1.9  2.   2.1  2.2  2.3  2.4
  2.5  2.6  2.7  2.8  2.9  3.   3.1  3.2  3.3  3.4  3.5  3.6  3.7  3.8  3.9
  4.   4.1  4.2  4.3  4.4  4.5  4.6  4.7  4.8  4.9]
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
      Ahora que ya la tenemos accesible la podemos usar desde R. Por ejemplo, vamos a usar la función <code>sum</code> en R que suma los elementos pero directamente desde R:</p>
    </div>
  </div>
</div>

<div>
  <div>
    <div>
      <div>
        <div class=" highlight hl-ipython3">
          <pre><span class="nb">print</span><span class="p">(</span><span class="n">ro</span><span class="o">.</span><span class="n">r</span><span class="p">(</span><span class="s">&#39;sum(variable_ahora_en_r)&#39;</span><span class="p">))</span>
<span class="nb">print</span><span class="p">(</span><span class="n">np</span><span class="o">.</span><span class="n">sum</span><span class="p">(</span><span class="n">variable_r_creada_desde_python</span><span class="p">))</span>
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
          <pre>[ 118.]
118.0
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
      Perfecto, ya sabemos, de forma muy sencilla y básica, como podemos usar R desde Python, como podemos pasar información desde R hacia Python y desde Python hacia R. ¡¡¡Esto es muy poderoso!!!, estamos juntando lo mejor de dos mundos, la solidez de las herramientas científicas de Python con la funcionalidad especializada que nos pueden aportar algunas librerías de R no disponibles en otros ámbitos.</p>
    </div>
  </div>
</div>

<div>
  <div>
  </div>
  
  <div>
    <div>
      <h1 id="Trabajando-de-forma-h&#237;brida-entre-Python-y-R">
        Trabajando de forma h&#237;brida entre Python y R<a class="anchor-link" href="#Trabajando-de-forma-h&#237;brida-entre-Python-y-R">&#182;</a>
      </h1>
    </div>
  </div>
</div>

<div>
  <div>
  </div>
  
  <div>
    <div>
      Vamos a empezar importando la librería <em>extRemes</em> de R:</p>
    </div>
  </div>
</div>

<div>
  <div>
    <div>
      <div>
        <div class=" highlight hl-ipython3">
          <pre><span class="c"># Importamos la librería extRemes de R</span>
<span class="kn">from</span> <span class="nn">rpy2.robjects.packages</span> <span class="k">import</span> <span class="n">importr</span>
<span class="n">extremes</span> <span class="o">=</span> <span class="n">importr</span><span class="p">(</span><span class="s">&#39;extRemes&#39;</span><span class="p">)</span>
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
      En la anterior celda hemos hecho lo siguiente:</p>
    </div>
  </div>
</div>

<div>
  <div>
  </div>
  
  <div>
    <div>
      <ul>
        <li>
          <code>from rpy2.robjects.packages import importr</code>, La función <code>importr</code> nos servirá para importar las librerías R
        </li>
        <li>
          <code>extremes = importr('extRemes')</code>, de esta forma importamos la librería <code>extRemes</code> de R, sería equivalente a hacer en R <code>library(extRemes)</code>.
        </li>
      </ul>
    </div>
  </div>
</div>

<div>
  <div>
  </div>
  
  <div>
    <div>
      Leemos datos con pandas. En el mismo repo donde está este notebook está también un fichero de texto con datos que creé a priori. Supuestamente son datos horarios de velocidad del viento por lo que vamos a hacer análisis de valores extremos de velocidad del viento horaria.</p>
    </div>
  </div>
</div>

<div>
  <div>
    <div>
      <div>
        <div class=" highlight hl-ipython3">
          <pre><span class="n">data</span> <span class="o">=</span> <span class="n">pd</span><span class="o">.</span><span class="n">read_csv</span><span class="p">(</span><span class="s">&#39;datasets/Synthetic_data.txt&#39;</span><span class="p">,</span>
                   <span class="n">sep</span> <span class="o">=</span> <span class="s">&#39;\s*&#39;</span><span class="p">,</span> <span class="n">skiprows</span> <span class="o">=</span> <span class="mi">1</span><span class="p">,</span> <span class="n">parse_dates</span> <span class="o">=</span> <span class="p">[[</span><span class="mi"></span><span class="p">,</span> <span class="mi">1</span><span class="p">]],</span>
                   <span class="n">names</span> <span class="o">=</span> <span class="p">[</span><span class="s">&#39;date&#39;</span><span class="p">,</span><span class="s">&#39;time&#39;</span><span class="p">,</span><span class="s">&#39;wspd&#39;</span><span class="p">],</span> <span class="n">index_col</span> <span class="o">=</span> <span class="mi"></span><span class="p">)</span>
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
          <pre><span class="n">data</span><span class="o">.</span><span class="n">head</span><span class="p">(</span><span class="mi">3</span><span class="p">)</span>
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
          <div style="max-height:1000px;max-width:1500px;overflow:auto;">
            <table border="1" class="dataframe">
              <tr style="text-align: right;">
                <th>
                </th>
                
                <th>
                  wspd
                </th>
              </tr>
              
              <tr>
                <th>
                  date_time
                </th>
                
                <th>
                </th>
              </tr>
              
              <tr>
                <th>
                  1983-01-01 00:00:00
                </th>
                
                <td>
                  7.9
                </td>
              </tr>
              
              <tr>
                <th>
                  1983-01-01 01:00:00
                </th>
                
                <td>
                  8.2
                </td>
              </tr>
              
              <tr>
                <th>
                  1983-01-01 02:00:00
                </th>
                
                <td>
                  8.5
                </td>
              </tr>
            </table>
          </div>
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
      Extraemos los máximos anuales los cuales usaremos posteriormente dentro de R para hacer cálculo de valores extremos usando la <a href="https://en.wikipedia.org/wiki/Generalized_extreme_value_distribution">distribución generalizada de valores extremos (GEV)</a>:</p>
    </div>
  </div>
</div>

<div>
  <div>
    <div>
      <div>
        <div class=" highlight hl-ipython3">
          <pre><span class="n">max_y</span> <span class="o">=</span> <span class="n">data</span><span class="o">.</span><span class="n">wspd</span><span class="o">.</span><span class="n">groupby</span><span class="p">(</span><span class="n">pd</span><span class="o">.</span><span class="n">TimeGrouper</span><span class="p">(</span><span class="n">freq</span> <span class="o">=</span> <span class="s">&#39;A&#39;</span><span class="p">))</span><span class="o">.</span><span class="n">max</span><span class="p">()</span>
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
      Dibujamos los valores máximos anuales usando Pandas:</p>
    </div>
  </div>
</div>

<div>
  <div>
    <div>
      <div>
        <div class=" highlight hl-ipython3">
          <pre><span class="n">max_y</span><span class="o">.</span><span class="n">plot</span><span class="p">(</span><span class="n">kind</span> <span class="o">=</span> <span class="s">&#39;bar&#39;</span><span class="p">,</span> <span class="n">figsize</span> <span class="o">=</span> <span class="p">(</span><span class="mi">12</span><span class="p">,</span> <span class="mi">4</span><span class="p">))</span>
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
          <pre>&lt;matplotlib.axes._subplots.AxesSubplot at 0x10a923d0&gt;</pre>
        </div>
      </div>
      
      <div>
        <div>
        </div>
        
        <div>
          <img src="http://new.pybonacci.org/images/2015/06/wpid-Trabajando_con_Python_y_R1.png"
 />
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
      Referenciamos la funcionalidad <a href="http://cran.r-project.org/web/packages/extRemes/extRemes.pdf"><code>fevd</code> (<em>fit extreme value distribution</em>) dentro del paquete <code>extremes</code></a> de R para poder usarla directamente con los valores máximos que hemos obtenido usando Pandas y desde Python.</p>
    </div>
  </div>
</div>

<div>
  <div>
    <div>
      <div>
        <div class=" highlight hl-ipython3">
          <pre><span class="n">fevd</span> <span class="o">=</span> <span class="n">extremes</span><span class="o">.</span><span class="n">fevd</span>
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
      Como hemos comentado anteriormente, vamos a calcular los parámetros de la GEV usando el método de ajuste <code>GMLE</code> (<em>Generalised Maximum Lihelihood Estimation</em>) y los vamos a guardar directamente en una variable Python.</p>
    </div>
  </div>
</div>

<div>
  <div>
  </div>
  
  <div>
    <div>
      Veamos la ayuda antes:</p>
    </div>
  </div>
</div>

<div>
  <div>
    <div>
      <div>
        <div class=" highlight hl-ipython3">
          <pre><span class="nb">print</span><span class="p">(</span><span class="n">fevd</span><span class="o">.</span><span class="n">__doc__</span><span class="p">)</span>
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
          <pre>Python representation of an R function.
description
-----------


 Fit a univariate extreme value distribution functions (e.g., GEV, GP, PP, Gumbel, or Exponential) to data; possibly with covariates in the parameters.
 


fevd(
    x,
    data,
    threshold = rinterface.NULL,
    threshold_fun = ~,
    location_fun = ~,
    scale_fun = ~,
    shape_fun = ~,
    use_phi = False,
    type = c,
    method = c,
    initial = rinterface.NULL,
    span,
    units = rinterface.NULL,
    time_units = days,
    period_basis = year,
    na_action = &lt;rpy2.rinterface.SexpVector - Python:0x116D6C50 / R:0x0C4BB100&gt;,
    optim_args = rinterface.NULL,
    priorFun = rinterface.NULL,
    priorParams = rinterface.NULL,
    proposalFun = rinterface.NULL,
    proposalParams = rinterface.NULL,
    iter = 9999.0,
    weights = 1.0,
    blocks = rinterface.NULL,
    verbose = False,
)

x :  &#96;fevd&#96;: &#96;x&#96; can be a numeric vector, the name of a column of &#96;data&#96; or a formula giving the data to which the EVD is to be fit.  In the case of the latter two, the &#96;data&#96; argument must be specified, and must have appropriately named columns.&#96;plot&#96; and &#96;print&#96; method functions: any list object returned by &#96;fevd&#96;. ,

object :  A list object of class \dQuote{fevd} as returned by &#96;fevd&#96;. ,

data :  A data frame object with named columns giving the data to be fit, as well as any data necessary for modeling non-stationarity through the threshold and/or any of the parameters. ,

threshold :  numeric (single or vector).  If fitting a peak over threshold (POT) model (i.e., &#96;type&#96; = \dQuote{PP}, \dQuote{GP}, \dQuote{Exponential}) this is the threshold over which (non-inclusive) data (or excesses) are used to estimate the parameters of the distribution function.  If the length is greater than 1, then the length must be equal to either the length of &#96;x&#96; (or number of rows of &#96;data&#96;) or to the number of unique arguments in &#96;threshold.fun&#96;. ,

threshold.fun :  formula describing a model for the thresholds using columns from &#96;data&#96;.  Any valid formula will work.  &#96;data&#96; must be supplied if this argument is anything other than ~ 1.  Not for use with &#96;method&#96; \dQuote{Lmoments}. ,

location.fun :  formula describing a model for each parameter using columns from &#96;data&#96;.  &#96;data&#96; must be supplied if any of these arguments are anything other than ~ 1. ,

scale.fun :  formula describing a model for each parameter using columns from &#96;data&#96;.  &#96;data&#96; must be supplied if any of these arguments are anything other than ~ 1. ,

shape.fun :  formula describing a model for each parameter using columns from &#96;data&#96;.  &#96;data&#96; must be supplied if any of these arguments are anything other than ~ 1. ,

use.phi :  logical; should the log of the scale parameter be used in the numerical optimization (for &#96;method&#96; \dQuote{MLE}, \dQuote{GMLE} and \dQuote{Bayesian} only)?  For the ML and GML estimation, this may make things more stable for some data. ,

type :  &#96;fevd&#96;: character stating which EVD to fit.  Default is to fit the generalized extreme value (GEV) distribution function (df).&#96;plot&#96; method function: character describing which plot(s) is (are) desired.  Default is \dQuote{primary}, which makes a 2 by 2 panel of plots including the QQ plot of the data quantiles against the fitted model quantiles (&#96;type&#96; \dQuote{qq}), a QQ plot (\dQuote{qq2}) of quantiles from model-simulated data against the data, a density plot of the data along with the model fitted density (&#96;type&#96; \dQuote{density}) and a return level plot (&#96;type&#96; \dQuote{rl}). In the case of a stationary (fixed) model, the return level plot will show return levels calculated for return periods given by &#96;return.period&#96;, along with associated CIs (calculated using default &#96;method&#96; arguments depending on the estimation method used in the fit.  For non-stationary models, the data are plotted as a line along with associated effective return levels for return periods of 2, 20 and 100 years (unless &#96;return.period&#96; is specified by the user to other values.  Other possible values for &#96;type&#96; include \dQuote{hist}, which is similar to \dQuote{density}, but shows the histogram for the data and \dQuote{trace}, which is not used for L-moment fits.  In the case of MLE/GMLE, the trace yields a panel of plots that show the negative log-likelihood and gradient negative log-likelihood (note that the MLE gradient is currently used even for GMLE) for each of the estimated parameter(s); allowing one parameter to vary according to &#96;prange&#96;, while the others remain fixed at their estimated values.  In the case of Bayesian estimation, the \dQuote{trace} option creates a panel of plots showing the posterior df and MCMC trace for each parameter. ,

method :  &#96;fevd&#96;: character naming which type of estimation method to use.  Default is to use maximum likelihood estimation (MLE). ,

initial :  A list object with any named parameter component giving the initial value estimates for starting the numerical optimization (MLE/GMLE) or the MCMC iterations (Bayesian).  In the case of MLE/GMLE, it is best to obtain a good intial guess, and in the Bayesian case, it is perhaps better to choose poor initial estimates.  If NULL (default), then L-moments estimates and estimates based on Gumbel moments will be calculated, and whichever yields the lowest negative log-likelihood is used.  In the case of &#96;type&#96; \dQuote{PP}, an additional MLE/GMLE estimate is made for the generalized Pareto (GP) df, and parameters are converted to those of the Poisson Process (PP) model.  Again, the initial estimates yielding the lowest negative log-likelihoo value are used for the initial guess. ,

span :  single numeric giving the number of years (or other desired temporal unit) in the data set.  Only used for POT models, and only important in the estimation for the PP model, but important for subsequent estimates of return levels for any POT model.  If missing, it will be calculated using information from &#96;time.units&#96;. ,

units :  (optional) character giving the units of the data, which if given may be used subsequently (e.g., on plot axis labels, etc.). ,

time.units :  character string that must be one of \dQuote{hours}, \dQuote{minutes}, \dQuote{seconds}, \dQuote{days}, \dQuote{months}, \dQuote{years}, \dQuote{m/hour}, \dQuote{m/minute}, \dQuote{m/second}, \dQuote{m/day}, \dQuote{m/month}, or \dQuote{m/year}; where m is a number.  If &#96;span&#96; is missing, then this argument is used in determining the value of &#96;span&#96;.  It is also returned with the output and used subsequently for plot labelling, etc. ,

period.basis :  character string giving the units for the period.  Used only for plot labelling and naming output vectors from some of the method functions (e.g., for establishing what the period represents for the return period). ,

rperiods :  numeric vector giving the return period(s) for which it is desired to calculate the corresponding return levels. ,

period :  character string naming the units for the return period. ,

burn.in :  The first &#96;burn.in&#96; values are thrown out before calculating anything from the MCMC sample. ,

a :  when plotting empirical probabilies and such, the function &#96;ppoints&#96; is called, which has this argument &#96;a&#96;. ,

d :  numeric determining how to scale the rate parameter for the point process.  If NULL, the function will attempt to scale based on the values of &#96;period.basis&#96; and &#96;time.units&#96;, the first of which must be \dQuote{year} and the second of which must be one of \dQuote{days}, \dQuote{months}, \dQuote{years}, \dQuote{hours}, \dQuote{minutes} or \dQuote{seconds}.  If none of these are the case, then &#96;d&#96; should be specified, otherwise, it is not necessary. ,

density.args :  named list object containing arguments to the &#96;density&#96; and &#96;hist&#96; functions, respectively. ,

hist.args :  named list object containing arguments to the &#96;density&#96; and &#96;hist&#96; functions, respectively. ,

na.action :  function to be called to handle missing values.  Generally, this should remain at the default (na.fail), and the user should take care to impute missing values in an appropriate manner as it may have serious consequences on the results. ,

optim.args :  A list with named components matching exactly any arguments that the user wishes to specify to &#96;optim&#96;, which is used only for MLE and GMLE methods.  By default, the \dQuote{BFGS} method is used along with &#96;grlevd&#96; for the gradient argument.  Generally, the &#96;grlevd&#96; function is used for the &#96;gr&#96; option unless the user specifies otherwise, or the optimization method does not take gradient information. ,

priorFun :  character naming a prior df to use for methods GMLE and Bayesian.  The default for GMLE (not including Gumbel or Exponential types) is to use the one suggested by Martins and Stedinger (2000, 2001) on the shape parameter; a beta df on -0.5 to 0.5 with parameters &#96;p&#96; and &#96;q&#96;.  Must take &#96;x&#96; as its first argument for &#96;method&#96; \dQuote{GMLE}.  Optional arguments for the default function are &#96;p&#96; and &#96;q&#96; (see details section).The default for Bayesian estimation is to use normal distribution functions.  For Bayesian estimation, this function must take &#96;theta&#96; as its first argument.Note: if this argument is not NULL and &#96;method&#96; is set to \dQuote{MLE}, it will be changed to \dQuote{GMLE}. ,

priorParams :  named list containing any prior df parameters (where the list names are the same as the function argument names).  Default for GMLE (assuming the default function is used) is to use &#96;q&#96; = 6 and &#96;p&#96; = 9.  Note that in the Martins and Stedinger (2000, 2001) papers, they use a different EVD parametrization than is used here such that a positive shape parameter gives the upper bounded distribution instead of the heavy-tail one (as emloyed here).  To be consistent with these papers, &#96;p&#96; and &#96;q&#96; are reversed inside the code so that they have the same interpretation as in the papers.Default for Bayesian estimation is to use ML estimates for the means of each parameter (may be changed using &#96;m&#96;, which must be a vector of same length as the number of parameters to be estimated (i.e., if using the default prior df)) and a standard deviation of 10 for all other parameters (again, if using the default prior df, may be changed using &#96;v&#96;, which must be a vector of length equal to the number of parameters). ,

proposalFun :  For Bayesian estimation only, this is a character naming a function used to generate proposal parameters at each iteration of the MCMC.  If NULL (default), a random walk chain is used whereby if theta.i is the current value of the parameter, the proposed new parameter theta.star is given by theta.i + z, where z is drawn at random from a normal df. ,

proposalParams :  A named list object describing any optional arguments to the &#96;proposalFun&#96; function.  All functions must take argument &#96;p&#96;, which must be a vector of the parameters, and &#96;ind&#96;, which is used to identify which parameter is to be proposed.  The default &#96;proposalFun&#96; function takes additional arguments &#96;mean&#96; and &#96;sd&#96;, which must be vectors of length equal to the number of parameters in the model (default is to use zero for the mean of z for every parameter and 0.1 for its standard deviation). ,

iter :  Used only for Bayesian estimation, this is the number of MCMC iterations to do. ,

weights :  numeric of length 1 or n giving weights to be applied     in the likelihood calculations (e.g., if there are data points to     be weighted more/less heavily than others). ,

blocks :  An optional list containing information required to fit point process models in a computationally-efficient manner by using only the exceedances and not the observations below the threshold(s). See details for further information.       ,

FUN :  character string naming a function to use to estimate the parameters from the MCMC sample.  The function is applied to each column of the &#96;results&#96; component of the returned &#96;fevd&#96; object. ,

verbose :  logical; should progress information be printed to the screen?  If TRUE, for MLE/GMLE, the argument &#96;trace&#96; will be set to 6 in the call to &#96;optim&#96;. ,

prange :  matrix whose columns are numeric vectors of length two for each parameter in the model giving the parameter range over which trace plots should be made.  Default is to use either +/- 2 * std. err. of the parameter (first choice) or, if the standard error cannot be calculated, then +/- 2 * log2(abs(parameter)).  Typically, these values seem to work very well for these plots. ,

... :  Not used by most functions here.  Optional arguments to &#96;plot&#96; for the various &#96;plot&#96; method functions.In the case of the &#96;summary&#96; method functions, the logical argument &#96;silent&#96; may be passed to suppress (if TRUE) printing any information to the screen. ,

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
      Y ahora vamos a hacer un cálculo sin meternos mucho en todas las opciones posibles.</p>
    </div>
  </div>
</div>

<div>
  <div>
    <div>
      <div>
        <div class=" highlight hl-ipython3">
          <pre><span class="n">res</span> <span class="o">=</span> <span class="n">fevd</span><span class="p">(</span><span class="n">max_y</span><span class="o">.</span><span class="n">values</span><span class="p">,</span> <span class="nb">type</span> <span class="o">=</span> <span class="s">"GEV"</span><span class="p">,</span> <span class="n">method</span> <span class="o">=</span> <span class="s">"GMLE"</span><span class="p">)</span>
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
      ¿Qué estructura tiene la variable <code>res</code> que acabamos de crear y que tiene los resultados del ajuste?</p>
    </div>
  </div>
</div>

<div>
  <div>
    <div>
      <div>
        <div class=" highlight hl-ipython3">
          <pre><span class="nb">print</span><span class="p">(</span><span class="nb">type</span><span class="p">(</span><span class="n">res</span><span class="p">))</span>
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
          <pre>&lt;class ';rpy2.robjects.vectors.ListVector';&gt;
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
          <pre><span class="nb">print</span><span class="p">(</span><span class="n">res</span><span class="o">.</span><span class="n">r_repr</span><span class="p">)</span>
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
          <pre>&lt;bound method ListVector.r_repr of &lt;ListVector - Python:0x10AB8878 / R:0x0CA9B458&gt;
[Vector, ndarray, ndarray, ..., ndarray, ListV..., ListV...]
  call: &lt;class ';rpy2.robjects.vectors.Vector';&gt;
  &lt;Vector - Python:0x10AB8418 / R:0x0CB2FFB4&gt;
[RNULLType, Vector, Vector, Vector]
  data.name: &lt;class ';numpy.ndarray';&gt;
  array([';structure(c(22.2, 25.5, 21.5, 22.5, 23.7, 22.5, 21.7, 29.7, 24.2, ';,
       ';23.8, 28.1, 23.4, 23.7, 25.6, 23.2, 24.9, 22.8, 24.6, 22.3, 25.5, ';,
       ';22.6, 24, 20.8, 23.5, 24.4, 24.1, 25.1, 19.4, 22.8, 24.2, 25, ';,
       ';25.3), .Dim = 32L)';, ';';], 
      dtype=';&lt;U66';)
  weights: &lt;class ';numpy.ndarray';&gt;
  array([ 1.])
  ...
  call: &lt;class ';numpy.ndarray';&gt;
  array([';location';, ';scale';, ';shape';], 
      dtype=';&lt;U8';)
&lt;ListVector - Python:0x10AB8878 / R:0x0CA9B458&gt;
[Vector, ndarray, ndarray, ..., ndarray, ListV..., ListV...]
&lt;ListVector - Python:0x10AB8878 / R:0x0CA9B458&gt;
[Vector, ndarray, ndarray, ..., ndarray, ListV..., ListV...]&gt;
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
      Según nos indica lo anterior, ahora <code>res</code> es un vector que está compuesto de diferentes elementos. Los vectores pueden tener un nombre para todos o algunos de los elementos. Para acceder a estor nombres podemos hacer:</p>
    </div>
  </div>
</div>

<div>
  <div>
    <div>
      <div>
        <div class=" highlight hl-ipython3">
          <pre><span class="n">res</span><span class="o">.</span><span class="n">names</span>
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
          <pre>array([';call';, ';data.name';, ';weights';, ';in.data';, ';x';, ';priorFun';,
       ';priorParams';, ';method';, ';type';, ';period.basis';, ';par.models';,
       ';const.loc';, ';const.scale';, ';const.shape';, ';n';, ';na.action';,
       ';parnames';, ';results';, ';initial.results';], 
      dtype=';&lt;U15';)</pre>
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
      Según el output anterior, parece que hay un nombre <code>results</code>, ahí es donde se guardan los valores del ajuste, los estimadores. Para acceder al mismo podemos hacerlo de diferentes formas. Con Python tendriamos que saber el índice y acceder de forma normal (<code>__getitem__()</code>). Existe una forma alternativa usando el método <code>rx</code> que nos permite acceder directamente con el nombre:</p>
    </div>
  </div>
</div>

<div>
  <div>
    <div>
      <div>
        <div class=" highlight hl-ipython3">
          <pre><span class="n">results</span> <span class="o">=</span> <span class="n">res</span><span class="o">.</span><span class="n">rx</span><span class="p">(</span><span class="s">&#39;results&#39;</span><span class="p">)</span>
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
          <pre><span class="nb">print</span><span class="p">(</span><span class="n">results</span><span class="o">.</span><span class="n">r_repr</span><span class="p">)</span>
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
          <pre>&lt;bound method ListVector.r_repr of &lt;ListVector - Python:0x10ABBCB0 / R:0x0CBFBC40&gt;
[ListVector]
&lt;ListVector - Python:0x10ABBCB0 / R:0x0CBFBC40&gt;
[ListVector]&gt;
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
      Parece que tenemos un único elemento:</p>
    </div>
  </div>
</div>

<div>
  <div>
    <div>
      <div>
        <div class=" highlight hl-ipython3">
          <pre><span class="n">results</span> <span class="o">=</span> <span class="n">results</span><span class="p">[</span><span class="mi"></span><span class="p">]</span>
<span class="n">results</span><span class="o">.</span><span class="n">r_repr</span>
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
          <pre>&lt;bound method ListVector.r_repr of &lt;ListVector - Python:0x10ABF490 / R:0x0C851BA0&gt;
[ndarray, ndarray, ndarray, ..., RNULL..., ndarray, ListV...]
  par: &lt;class ';numpy.ndarray';&gt;
  array([ 23.06394152,   1.75769129,  -0.16288164])
  value: &lt;class ';numpy.ndarray';&gt;
  array([  1.00000000e+16])
  counts: &lt;class ';numpy.ndarray';&gt;
  array([1, 1], dtype=int32)
  ...
  par: &lt;class ';rpy2.rinterface.RNULLType';&gt;
  rpy2.rinterface.NULL
  value: &lt;class ';numpy.ndarray';&gt;
  array([[ 0.,  0.,  0.],
       [ 0.,  0.,  0.],
       [ 0.,  0.,  0.]])
&lt;ListVector - Python:0x10ABF490 / R:0x0C851BA0&gt;
[ndarray, ndarray, ndarray, ..., RNULL..., ndarray, ListV...]&gt;</pre>
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
      Vemos ahora que <code>results</code> tiene un elemento con nombre <code>par</code> donde se guardan los valores de los estimadores del ajuste a la GEV que hemos obtenido usando GMLE. Vamos a obtener finalmente los valores de los estimadores:</p>
    </div>
  </div>
</div>

<div>
  <div>
    <div>
      <div>
        <div class=" highlight hl-ipython3">
          <pre><span class="n">location</span><span class="p">,</span> <span class="n">scale</span><span class="p">,</span> <span class="n">shape</span> <span class="o">=</span> <span class="n">results</span><span class="o">.</span><span class="n">rx</span><span class="p">(</span><span class="s">&#39;par&#39;</span><span class="p">)[</span><span class="mi"></span><span class="p">][:]</span>
<span class="nb">print</span><span class="p">(</span><span class="n">location</span><span class="p">,</span> <span class="n">scale</span><span class="p">,</span> <span class="n">shape</span><span class="p">)</span>
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
          <pre>23.0639415199 1.75769128743 -0.162881636772
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
      <h1 id="Funcion-m&#225;gica-para-R-(antigua-rmagic)">
        Funcion m&#225;gica para R (antigua <code>rmagic</code>)<a class="anchor-link" href="#Funcion-m&#225;gica-para-R-(antigua-rmagic)">&#182;</a>
      </h1>
    </div>
  </div>
</div>

<div>
  <div>
  </div>
  
  <div>
    <div>
      Usamos la antigua función mágica <code>rmagic</code> que ahora se activará en el notebook de la siguiente forma:</p>
    </div>
  </div>
</div>

<div>
  <div>
    <div>
      <div>
        <div class=" highlight hl-ipython3">
          <pre><span class="o">%</span><span class="k">load_ext</span> rpy2.ipython
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
      Veamos como funciona la functión mágica de R:</p>
    </div>
  </div>
</div>

<div>
  <div>
    <div>
      <div>
        <div class=" highlight hl-ipython3">
          <pre><span class="n">help</span><span class="p">(</span><span class="n">rpy2</span><span class="o">.</span><span class="n">ipython</span><span class="o">.</span><span class="n">rmagic</span><span class="o">.</span><span class="n">RMagics</span><span class="o">.</span><span class="n">R</span><span class="p">)</span>
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
          <pre>Help on function R in module rpy2.ipython.rmagic:

R(self, line, cell=None, local_ns=None)
    ::
    
      %R [-i INPUT] [-o OUTPUT] [-n] [-w WIDTH] [-h HEIGHT] [-p POINTSIZE]
             [-b BG] [--noisolation] [-u {px,in,cm,mm}] [-r RES]
             

<pre><code></code></pre>]
    
    Execute code in R, optionally returning results to the Python runtime.
    
    In line mode, this will evaluate an expression and convert the returned
    value to a Python object.  The return value is determined by rpy2';s
    behaviour of returning the result of evaluating the final expression.
    
    Multiple R expressions can be executed by joining them with semicolons::
    
        In [9]: %R X=c(1,4,5,7); sd(X); mean(X)
        Out[9]: array([ 4.25])
    
    In cell mode, this will run a block of R code. The resulting value
    is printed if it would printed be when evaluating the same code
    within a standard R REPL.
    
    Nothing is returned to python by default in cell mode::
    
        In [10]: %%R
           ....: Y = c(2,4,3,9)
           ....: summary(lm(Y~X))
    
        Call:
        lm(formula = Y ~ X)
    
        Residuals:
            1     2     3     4
         0.88 -0.24 -2.28  1.64
    
        Coefficients:
                    Estimate Std. Error t value Pr(&gt;|t|)
        (Intercept)   0.0800     2.3000   0.035    0.975
        X             1.0400     0.4822   2.157    0.164
    
        Residual standard error: 2.088 on 2 degrees of freedom
        Multiple R-squared: 0.6993,Adjusted R-squared: 0.549
        F-statistic: 4.651 on 1 and 2 DF,  p-value: 0.1638
    
    In the notebook, plots are published as the output of the cell::
    
        %R plot(X, Y)
    
    will create a scatter plot of X bs Y.
    
    If cell is not None and line has some R code, it is prepended to
    the R code in cell.
    
    Objects can be passed back and forth between rpy2 and python via the -i -o flags in line::
    
        In [14]: Z = np.array([1,4,5,10])
    
        In [15]: %R -i Z mean(Z)
        Out[15]: array([ 5.])
    
        In [16]: %R -o W W=Z*mean(Z)
        Out[16]: array([  5.,  20.,  25.,  50.])
    
        In [17]: W
        Out[17]: array([  5.,  20.,  25.,  50.])
    
    The return value is determined by these rules:
    
    * If the cell is not None (i.e., has contents), the magic returns None.
    
    * If the final line results in a NULL value when evaluated
      by rpy2, then None is returned.
    
    * No attempt is made to convert the final value to a structured array.
      Use %Rget to push a structured array.
    
    * If the -n flag is present, there is no return value.
    
    * A trailing ';;'; will also result in no return value as the last
      value in the line is an empty string.
    
    optional arguments:
      -i INPUT, --input INPUT
                            Names of input variable from shell.user_ns to be
                            assigned to R variables of the same names after
                            calling self.pyconverter. Multiple names can be passed
                            separated only by commas with no whitespace.
      -o OUTPUT, --output OUTPUT
                            Names of variables to be pushed from rpy2 to
                            shell.user_ns after executing cell body (rpy2';s
                            internal facilities will apply ri2ro as appropriate).
                            Multiple names can be passed separated only by commas
                            with no whitespace.
      -n, --noreturn        Force the magic to not return anything.
    
    Plot:
      Arguments to plotting device
    
      -w WIDTH, --width WIDTH
                            Width of plotting device in R.
      -h HEIGHT, --height HEIGHT
                            Height of plotting device in R.
      -p POINTSIZE, --pointsize POINTSIZE
                            Pointsize of plotting device in R.
      -b BG, --bg BG        Background of plotting device in R.
    
    SVG:
      SVG specific arguments
    
      --noisolation         Disable SVG isolation in the Notebook. By default,
                            SVGs are isolated to avoid namespace collisions
                            between figures.Disabling SVG isolation allows to
                            reference previous figures or share CSS rules across a
                            set of SVGs.
    
    PNG:
      PNG specific arguments
    
      -u &lt;{px,in,cm,mm}&gt;, --units &lt;{px,in,cm,mm}&gt;
                            Units of png plotting device sent as an argument to
                            *png* in R. One of ["px", "in", "cm", "mm"].
      -r RES, --res RES     Resolution of png plotting device sent as an argument
                            to *png* in R. Defaults to 72 if *units* is one of
                            ["in", "cm", "mm"].
      code

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
      A veces, será más simple usar la función mágica para interactuar con R. Veamos un ejemplo donde le pasamos a R el valor obtenido de la función <code>fevd</code> del paquete <code>extRemes</code> de R que he usado anteriormente y corremos cierto código directamente desde R sin tener que usar <code>ro.r</code>.</p>
    </div>
  </div>
</div>

<div>
  <div>
    <div>
      <div>
        <div class=" highlight hl-ipython3">
          <pre><span class="o">%</span><span class="k">R</span> -i res plot.fevd(res)
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
          <img src="http://new.pybonacci.org/images/2015/06/wpid-Trabajando_con_Python_y_R2.png"
 />
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
      En la anterior celda de código le he pasado como parámetro de entrada (<code>- i res</code>) la variable <code>res</code> que había obtenido anteriormente para que esté disponible desde R. y he ejecutado código R puro (<code>plot.fevd(res)</code>).</p>
    </div>
  </div>
</div>

<div>
  <div>
  </div>
  
  <div>
    <div>
      Si lo anterior lo quiero hacer con rpy2 puedo hacer lo siquiente:</p> 
      
      <p class="alert alert-info">
        CUIDADO, la siguiente celda de código puede provocar que se reinicialice el notebook y se rompa la sesión. Si has hecho cambios en el notebook guárdalos antes de ejecutar la celda, por lo que pueda pasar...
      </p>
    </div>
  </div>
</div>

<div>
  <div>
    <div>
      <div>
        <div class=" highlight hl-ipython3">
          <pre><span class="n">ro</span><span class="o">.</span><span class="n">globalenv</span><span class="p">[</span><span class="s">&#39;res&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="n">res</span>
<span class="n">ro</span><span class="o">.</span><span class="n">r</span><span class="p">(</span><span class="s">"plot.fevd(res)"</span><span class="p">)</span>
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
          <pre>rpy2.rinterface.NULL</pre>
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
      Lo anterior me bloquea el notebook y me 'rompe' la sesión (<a href="https://bitbucket.org/rpy2/rpy2/issues?q=windows">en windows, al menos</a>) ya que la ventana de gráficos se abre de forma externa... Por tanto, una buena opción para trabajar de forma interactiva con Python y R de forma conjunta y que no se 'rompa' nada es usar tanto rpy2 como su extensión para el notebook de Jupyter (dejaremos de llamarlo IPython poco a poco).</p>
    </div>
  </div>
</div>

<div>
  <div>
  </div>
  
  <div>
    <div>
      <h1 id="Usando-Python-y-R-combinando-rpy2-y-la-funci&#243;n-m&#225;gica">
        Usando Python y R combinando rpy2 y la funci&#243;n m&#225;gica<a class="anchor-link" href="#Usando-Python-y-R-combinando-rpy2-y-la-funci&#243;n-m&#225;gica">&#182;</a>
      </h1>
    </div>
  </div>
</div>

<div>
  <div>
  </div>
  
  <div>
    <div>
      Vamos a combinar las dos formas de trabajar con rpy2 en el siguiente ejemplo:</p>
    </div>
  </div>
</div>

<div>
  <div>
    <div>
      <div>
        <div class=" highlight hl-ipython3">
          <pre><span class="n">metodos</span> <span class="o">=</span> <span class="p">[</span><span class="s">"MLE"</span><span class="p">,</span> <span class="s">"GMLE"</span><span class="p">]</span>
<span class="n">tipos</span> <span class="o">=</span> <span class="p">[</span><span class="s">"GEV"</span><span class="p">,</span> <span class="s">"Gumbel"</span><span class="p">]</span>
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
      Lo que vamos a hacer es calcular los parámetros del ajuste usando la distribución GEV y Gumbel, que es un caso especial de la GEV. El ajuste lo calculamos usando tanto MLE como GMLE. Además de mostrar los valores resultantes del ajuste para los estimadores vamos a mostrar el dibujo de cada uno de los ajustes y algunos test de bondad. Usamos Python para toda la maquinaria de los bucles, usamos rpy2 para obtener los estimadores y usamos la función mágica de rpy2 para mostrar los gráficos del resultado.</p>
    </div>
  </div>
</div>

<div>
  <div>
    <div>
      <div>
        <div class=" highlight hl-ipython3">
          <pre><span class="k">for</span> <span class="n">t</span> <span class="ow">in</span> <span class="n">tipos</span><span class="p">:</span>
    <span class="k">for</span> <span class="n">m</span> <span class="ow">in</span> <span class="n">metodos</span><span class="p">:</span>
        <span class="nb">print</span><span class="p">(</span><span class="s">&#39;tipo de ajuste: &#39;</span><span class="p">,</span> <span class="n">t</span><span class="p">)</span>
        <span class="nb">print</span><span class="p">(</span><span class="s">&#39;método de ajuste: &#39;</span><span class="p">,</span> <span class="n">m</span><span class="p">)</span>
        <span class="n">res</span> <span class="o">=</span> <span class="n">fevd</span><span class="p">(</span><span class="n">max_y</span><span class="o">.</span><span class="n">values</span><span class="p">,</span> <span class="n">method</span> <span class="o">=</span> <span class="n">m</span><span class="p">,</span> <span class="nb">type</span> <span class="o">=</span> <span class="n">t</span><span class="p">)</span>
        <span class="k">if</span> <span class="n">m</span> <span class="o">==</span> <span class="s">"Bayesian"</span><span class="p">:</span>
            <span class="nb">print</span><span class="p">(</span><span class="n">res</span><span class="o">.</span><span class="n">rx</span><span class="p">(</span><span class="s">&#39;results&#39;</span><span class="p">)[</span><span class="mi"></span><span class="p">][</span><span class="o">-</span><span class="mi">1</span><span class="p">][</span><span class="mi"></span><span class="p">:</span><span class="o">-</span><span class="mi">2</span><span class="p">])</span>
        <span class="k">elif</span> <span class="n">m</span> <span class="o">==</span> <span class="s">"Lmoments"</span><span class="p">:</span>
            <span class="nb">print</span><span class="p">(</span><span class="n">res</span><span class="o">.</span><span class="n">rx</span><span class="p">(</span><span class="s">&#39;results&#39;</span><span class="p">)[</span><span class="mi"></span><span class="p">])</span>
        <span class="k">else</span><span class="p">:</span>
            <span class="nb">print</span><span class="p">(</span><span class="n">res</span><span class="o">.</span><span class="n">rx</span><span class="p">(</span><span class="s">&#39;results&#39;</span><span class="p">)[</span><span class="mi"></span><span class="p">]</span><span class="o">.</span><span class="n">rx</span><span class="p">(</span><span class="s">&#39;par&#39;</span><span class="p">)[</span><span class="mi"></span><span class="p">][:])</span>
        <span class="o">%</span><span class="k">R</span> -i res plot.fevd(res)
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
          <pre>tipo de ajuste:  GEV
método de ajuste:  MLE
[ 23.05170779   1.80858528  -0.14979836]
</pre>
        </div>
      </div>
      
      <div>
        <div>
        </div>
        
        <div>
          <img src="http://new.pybonacci.org/images/2015/06/wpid-Trabajando_con_Python_y_R3.png"
 />
        </div>
      </div>
      
      <div>
        <div>
        </div>
        
        <div>
          <pre>tipo de ajuste:  GEV
método de ajuste:  GMLE
[ 23.06394152   1.75769129  -0.16288164]
</pre>
        </div>
      </div>
      
      <div>
        <div>
        </div>
        
        <div>
          <img src="http://new.pybonacci.org/images/2015/06/wpid-Trabajando_con_Python_y_R4.png"
 />
        </div>
      </div>
      
      <div>
        <div>
        </div>
        
        <div>
          <pre>tipo de ajuste:  Gumbel
método de ajuste:  MLE
[ 22.90587606   1.81445179]
</pre>
        </div>
      </div>
      
      <div>
        <div>
        </div>
        
        <div>
          <img src="http://new.pybonacci.org/images/2015/06/wpid-Trabajando_con_Python_y_R5.png"
 />
        </div>
      </div>
      
      <div>
        <div>
        </div>
        
        <div>
          <pre>tipo de ajuste:  Gumbel
método de ajuste:  GMLE
[ 22.90587606   1.81445179]
</pre>
        </div>
      </div>
      
      <div>
        <div>
        </div>
        
        <div>
          <img src="http://new.pybonacci.org/images/2015/06/wpid-Trabajando_con_Python_y_R6.png"
 />
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
      <h1 id="Comentarios-finales">
        Comentarios finales<a class="anchor-link" href="#Comentarios-finales">&#182;</a>
      </h1>
    </div>
  </div>
</div>

<div>
  <div>
  </div>
  
  <div>
    <div>
      Espero que este microtutorial os valga, al menos, para conocer rpy2 y la potencia que os puede llegar a aportar a vuestros análisis 'pythónicos'. Como resumen:</p> 
      
      <ul>
        <li>
          Tenemos en nuestras manos una herramienta muy poderosa.
        </li>
        <li>
          Rpy2 puede estar poco madura en algún aspecto aunque ha mejorado bastante con respecto a alguna versión de rpy2 que usé anteriormente.
        </li>
        <li>
          También podéis usar directamente <a href="https://github.com/IRkernel/IRkernel">R como kernel</a>, aunque perdéis la interacción con Python. También puede ocurrir que la instalación os haga perder mucho el tiempo <a href="https://github.com/IRkernel/IRkernel/issues/54">para poder hacerlo funcionar</a> si os veis obligados a usarlo desde windows.
        </li>
        <li>
          En la elaboración de este microtutorial la consola de R donde iba haciendo algunas pruebas simples se me ha 'roto' muchísimas más veces de las que consideraría aceptables. No se puede quedar colgada, cerrar,..., seis o siete veces en media hora una consola haciendo cosas simples. Eso hace que si quieres usar R de forma interactiva debas usar alternativas como Jupyter, RStudio u otros que desconozco ya que la consola oficial no está 'ni pa pipas' (por lo menos en Windows, el sistema operativo con más usuarios potenciales, mal que me pese).
        </li>
        <li>
          Sigo manteniendo muchas reservas respecto a R como Lenguaje de Programación (en mayúsculas) por lo que si puedo limitar su uso a alguna librería especializada que necesito y a la que pueda acceder con rpy2 es lo que seguiré haciendo (<em><a href="http://www.burns-stat.com/pages/Tutor/R_inferno.pdf">If you are using R and you think you're in hell, this is a map for you</a>.</em>)
        </li>
      </ul>
    </div>
  </div>
</div>

# Y el notebook...[&#182;](#y-el-notebook){.anchor-link} {#y-el-notebook}

En el caso de que queráis trastear con el notebook lo podéis descargar desde [aquí](http://nbviewer.ipython.org/github/Pybonacci/notebooks/tree/master/Trabajando_con_R_Python/).

También podéis [descargar todos los notebooks desde nuestro repo oficial de notebooks](https://github.com/Pybonacci/notebooks).