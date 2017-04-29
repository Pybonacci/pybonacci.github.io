---
title: C elemental, querido Cython
date: 2015-03-09T00:47:23+00:00
author: Kiko Correoso
slug: c-elemental-querido-cython
tags: c, cython, numba, performance, pypy, rendimiento

<div>
  <div>
  </div>
  
  <div>
    <div>
      <h1 id="Cython,-que-no-CPython">
        Cython, que no CPython<a class="anchor-link" href="#Cython,-que-no-CPython">&#182;</a>
      </h1>
    </div>
  </div>
</div>

<div>
  <div>
  </div>
  
  <div>
    <div>
      No, no nos hemos equivocado en el título, hoy vamos a hablar de Cython.<br /> ¿Qué es Cython?<br /> Cython son dos cosas:</p> 
      
      <ul>
        <li>
          Por una parte, Cython es un lenguaje de programación (un superconjunto de Python) que une Python con el sistema de tipado estático de C y C++.
        </li>
        <li>
          Por otra parte, <code>cython</code> es un compilador que traduce codigo fuente escrito en Cython en eficiente código C o C++. El código resultante se podría usar como una extensión Python o como un ejecutable.
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
      ¡Guau! ¿Cómo os habéis quedado?</p>
    </div>
  </div>
</div>

<div>
  <div>
  </div>
  
  <div>
    <div>
      Lo que se pretende es, básicamente, aprovechar las fortalezas de Python y C, combinar una sintaxis sencilla con el poder y la velocidad.</p>
    </div>
  </div>
</div>

<div>
  <div>
  </div>
  
  <div>
    <div>
      Salvando algunas <a href="http://docs.cython.org/src/userguide/limitations.html#cython-limitations">excepciones</a>, el código Python (tanto Python 2 como Python 3) es código Cython válido. Además, Cython añade una serie de palabras clave para poder usar el sistema de tipado de C con Python y que el compilador <code>cython</code> pueda generar código C eficiente.</p>
    </div>
  </div>
</div>

<div>
  <div>
  </div>
  
  <div>
    <div>
      Pero, ¿quién usa Cython?<br /> Pues mira, igual no lo sabes pero seguramente estés usando Cython todos los días. Sage tiene casi medio millón de líneas de Cython (que se dice pronto), Scipy y Pandas más de 20000, scikit-learn unas 15000,...</p>
    </div>
  </div>
</div>

<div>
  <div>
  </div>
  
  <div>
    <div>
      <h1 id="&#191;Nos-empezamos-a-meter-en-harina?">
        &#191;Nos empezamos a meter en harina?<a class="anchor-link" href="#&#191;Nos-empezamos-a-meter-en-harina?">&#182;</a>
      </h1>
    </div>
  </div>
</div>

<div>
  <div>
  </div>
  
  <div>
    <div>
      La idea principal de este primer acercamiento a Cython será empezar con un código Python que sea nuestro cuello de botella e iremos creando versiones que sean cada vez más rápidas, o eso intentaremos.</p>
    </div>
  </div>
</div>

<div>
  <div>
  </div>
  
  <div>
    <div>
      Por ejemplo, imaginemos que tenemos que detectar valores mínimos locales dentro de una malla. Los valores mínimos deberán ser simplemente valores más bajos que los que haya en los 8 nodos de su entorno inmediato. En el siguiente gráfico, el nodo en verde será un nodo con un mínimo y en su entorno son todo valores superiores:</p> 
      
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
    </div>
  </div>
</div>

<div>
  <div>
  </div>
  
  <div>
    <div>
      [INCISO] Los números y porcentajes que veáis a continuación pueden variar levemente dependiendo de la máquina donde se ejecute. Tomad los valores como aproximativos.</p>
    </div>
  </div>
</div>

<div>
  <div>
  </div>
  
  <div>
    <div>
      <h1 id="Setup">
        Setup<a class="anchor-link" href="#Setup">&#182;</a>
      </h1>
    </div>
  </div>
</div>

<div>
  <div>
  </div>
  
  <div>
    <div>
      Como siempre, importamos algunas librerías antes de empezar a picar código:</p>
    </div>
  </div>
</div>

<div>
  <div>
    <div>
      <div>
        <div class=" highlight hl-ipython3">
          <pre><span class="kn">import</span> <span class="nn">numpy</span> <span class="k">as</span> <span class="nn">np</span>
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
      Creamos una matriz cuadrada relativamente grande (4 millones de elementos).</p>
    </div>
  </div>
</div>

<div>
  <div>
    <div>
      <div>
        <div class=" highlight hl-ipython3">
          <pre><span class="n">np</span><span class="o">.</span><span class="n">random</span><span class="o">.</span><span class="n">seed</span><span class="p">(</span><span class="mi"></span><span class="p">)</span>
<span class="n">data</span> <span class="o">=</span> <span class="n">np</span><span class="o">.</span><span class="n">random</span><span class="o">.</span><span class="n">randn</span><span class="p">(</span><span class="mi">2000</span><span class="p">,</span> <span class="mi">2000</span><span class="p">)</span>
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
      Ya tenemos los datos listos para empezar a trabajar.<br /> Vamos a crear una función en Python que busque los mínimos tal como los hemos definido.</p>
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
  </div>
  
  <div>
    <div>
      Veamos cuanto tarda esta función en mi máquina:</p>
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
          <pre>1 loops, best of 3: 3.63 s per loop
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
      Buff, tres segundos y pico en un i7... Si tengo que buscar los mínimos en 500 de estos casos me va a tardar casi media hora.</p>
    </div>
  </div>
</div>

<div>
  <div>
  </div>
  
  <div>
    <div>
      Por casualidad, vamos a probar numba a ver si es capaz de resolver el problema sin mucho esfuerzo, es código Python muy sencillo en el cual no usamos cosas muy 'extrañas' del lenguaje.</p>
    </div>
  </div>
</div>

<div>
  <div>
    <div>
      <div>
        <div class=" highlight hl-ipython3">
          <pre><span class="kn">from</span> <span class="nn">numba</span> <span class="k">import</span> <span class="n">jit</span>

<span class="nd">@jit</span>
<span class="k">def</span> <span class="nf">busca_min_numba</span><span class="p">(</span><span class="n">malla</span><span class="p">):</span>
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
          <pre><span class="o">%</span><span class="k">timeit</span> busca_min_numba(data)
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
          <pre>1 loops, best of 3: 4.97 s per loop
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
      Ooooops! Parece que la magia de numba no funciona aquí.</p>
    </div>
  </div>
</div>

<div>
  <div>
  </div>
  
  <div>
    <div>
      Vamos a especificar los tipos de entrada y de salida (y a modificar el output) a ver si mejora algo:</p>
    </div>
  </div>
</div>

<div>
  <div>
    <div>
      <div>
        <div class=" highlight hl-ipython3">
          <pre><span class="kn">from</span> <span class="nn">numba</span> <span class="k">import</span> <span class="n">jit</span>
<span class="kn">from</span> <span class="nn">numba</span> <span class="k">import</span> <span class="n">int32</span><span class="p">,</span> <span class="n">float64</span>

<span class="nd">@jit</span><span class="p">(</span><span class="n">int32</span><span class="p">[:,:](</span><span class="n">float64</span><span class="p">[:,:]))</span>
<span class="k">def</span> <span class="nf">busca_min_numba</span><span class="p">(</span><span class="n">malla</span><span class="p">):</span>
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

    <span class="k">return</span> <span class="n">np</span><span class="o">.</span><span class="n">array</span><span class="p">([</span><span class="n">minimosx</span><span class="p">,</span> <span class="n">minimosy</span><span class="p">],</span> <span class="n">dtype</span> <span class="o">=</span> <span class="n">np</span><span class="o">.</span><span class="n">int32</span><span class="p">)</span>
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
          <pre><span class="o">%</span><span class="k">timeit</span> busca_min_numba(data)
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
          <pre>1 loops, best of 3: 5.25 s per loop
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
      Pues parece que no, el resultado es del mismo pelo. Usando la opción <code>nopython</code> me casca un error un poco feo,...<br /> Habrá que seguir esperando a que numba esté un poco más maduro. En mis pocas experiencias no he conseguido aun el efecto que buscaba y en la mayoría de los casos obtengo errores muy crípticos. No es que no tenga confianza en la gente que está detrás, solo estoy diciendo que aun no está listo para 'producción'. Esto no pretende ser una guerra Cython/numba, solo he usado numba para ver si a pelo era capaz de mejorar algo el tema. Como no ha sido así, nos olvidamos de numba de momento.</p>
    </div>
  </div>
</div>

<div>
  <div>
  </div>
  
  <div>
    <div>
      <h1 id="Cythonizando,-que-es-gerundio-(toma-1).">
        Cythonizando, que es gerundio (toma 1).<a class="anchor-link" href="#Cythonizando,-que-es-gerundio-(toma-1).">&#182;</a>
      </h1>
    </div>
  </div>
</div>

<div>
  <div>
  </div>
  
  <div>
    <div>
      Lo más sencillo y evidente es usar directamente el compilador <code>cython</code> y ver si usando el código python tal cual es un poco más rápido. Para ello, vamos a usar las funciones mágicas que Cython pone a nuestra disposición en el notebook. Solo vamos a hablar de la función mágica <code>%%cython</code>, de momento, aunque hay otras.</p>
    </div>
  </div>
</div>

<div>
  <div>
    <div>
      <div>
        <div class=" highlight hl-ipython3">
          <pre><span class="c"># antes cythonmagic</span>
<span class="o">%</span><span class="k">load_ext</span> Cython
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
      EL comando <code>%%cython</code> nos permite escribir código Cython en una celda. Una vez que ejecutamos la celda, IPython se encarga de coger el código, crear un fichero de código Cython con extensión <em>.pyx</em>, compilarlo a C y, si todo está correcto, importar ese fichero para que todo esté disponible dentro del notebook.<br /> [INCISO] a la función mágica <code>%%cython</code> le podemos pasar una serie de argumentos. Veremos alguno en este análisis pero ahora vamos a definir uno que sirve para que podamos nombrar a la funcíon que se crea y compila al vuelo, <code>-n</code> o <code>--name</code>.</p>
    </div>
  </div>
</div>

<div>
  <div>
    <div>
      <div>
        <div class=" highlight hl-ipython3">
          <pre><span class="o">%%</span><span class="n">cython</span> <span class="o">--</span><span class="n">name</span> <span class="n">probandocython1</span>
<span class="k">import</span> <span class="nn">numpy</span> <span class="k">as</span> <span class="nn">np</span>

<span class="k">def</span> <span class="nf">busca_min_cython1</span><span class="p">(</span><span class="n">malla</span><span class="p">):</span>
    <span class="n">minimosx</span> <span class="o">=</span> <span class="p">[]</span>
    <span class="n">minimosy</span> <span class="o">=</span> <span class="p">[]</span>
    <span class="k">for</span> <span class="n">i</span> <span class="ow">in</span> <span class="nb">range</span><span class="p">(</span><span class="mf">1</span><span class="p">,</span> <span class="n">malla</span><span class="o">.</span><span class="n">shape</span><span class="p">[</span><span class="mf">1</span><span class="p">]</span><span class="o">-</span><span class="mf">1</span><span class="p">):</span>
        <span class="k">for</span> <span class="n">j</span> <span class="ow">in</span> <span class="nb">range</span><span class="p">(</span><span class="mf">1</span><span class="p">,</span> <span class="n">malla</span><span class="o">.</span><span class="n">shape</span><span class="p">[</span><span class="mf"></span><span class="p">]</span><span class="o">-</span><span class="mf">1</span><span class="p">):</span>
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
  </div>
  
  <div>
    <div>
      El fichero se creará dentro de la carpeta <em>cython</em> disponible dentro del directorio resultado de la función <code>get_ipython_cache_dir</code>. Veamos la localización del fichero en mi equipo:</p>
    </div>
  </div>
</div>

<div>
  <div>
    <div>
      <div>
        <div class=" highlight hl-ipython3">
          <pre><span class="kn">from</span> <span class="nn">IPython.utils.path</span> <span class="k">import</span> <span class="n">get_ipython_cache_dir</span>
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
          <pre><span class="nb">print</span><span class="p">(</span><span class="n">get_ipython_cache_dir</span><span class="p">()</span> <span class="o">+</span> <span class="s">&#39;/cython/probandocython1.c&#39;</span><span class="p">)</span>
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
          <pre>/home/kiko/.cache/ipython/cython/probandocython1.c
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
      No lo muestro por aquí porque el resultado son más de ¡¡2400!! líneas de código C.<br /> Veamos ahora lo que tarda.</p>
    </div>
  </div>
</div>

<div>
  <div>
    <div>
      <div>
        <div class=" highlight hl-ipython3">
          <pre><span class="o">%</span><span class="k">timeit</span> busca_min_cython1(data)
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
          <pre>1 loops, best of 3: 3.34 s per loop
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
      Bueno, parece que sin hacer mucho esfuerzo hemos conseguido ganar en torno a un 5% - 25% de rendimiento (dependerá del caso). No es gran cosa pero Cython es capaz de mucho más...</p>
    </div>
  </div>
</div>

<div>
  <div>
  </div>
  
  <div>
    <div>
      <h1 id="Cythonizando,-que-es-gerundio-(toma-2).">
        Cythonizando, que es gerundio (toma 2).<a class="anchor-link" href="#Cythonizando,-que-es-gerundio-(toma-2).">&#182;</a>
      </h1>
    </div>
  </div>
</div>

<div>
  <div>
  </div>
  
  <div>
    <div>
      En esta parte vamos a introducir una de las palabras clave que Cython introduce para extender Python, <code>cdef</code>. La palabra clave <code>cdef</code> sirve para 'tipar' estáticamente variables en Cython (luego veremos que se usa también para definir funciones). Por ejemplo:</p> 
      
      <div class="highlight">
        <pre><span class="n">cdef</span> <span class="nb">int</span> <span class="n">var1</span><span class="p">,</span> <span class="n">var2</span>
<span class="n">cdef</span> <span class="nb">float</span> <span class="n">var3</span>
</pre>
      </div>
    </div>
  </div>
</div>

<div>
  <div>
  </div>
  
  <div>
    <div>
      En el bloque de código de más arriba he creado dos variables de tipo entero, <code>var1</code> y <code>var2</code>, y una variable de tipo float, <code>var3</code>. Los <a href="http://docs.cython.org/src/userguide/language_basics.html#automatic-type-conversions">tipos anteriores son la nomenclatura C</a>.</p>
    </div>
  </div>
</div>

<div>
  <div>
  </div>
  
  <div>
    <div>
      Vamos a intentar usar <code>cdef</code> con algunos tipos de datos que tenemos dentro de nuestra función. Para empezar, veo evidente que tengo varias listas (<code>minimosx</code> y <code>minimosy</code>), tenemos los índices de los bucles (<code>i</code> y <code>j</code>) y voy a convertir los parámetros de los <code>range</code> en tipos estáticos (<code>ii</code> y <code>jj</code>):</p>
    </div>
  </div>
</div>

<div>
  <div>
    <div>
      <div>
        <div class=" highlight hl-ipython3">
          <pre><span class="o">%%</span><span class="n">cython</span> <span class="o">--</span><span class="n">name</span> <span class="n">probandocython2</span>
<span class="k">import</span> <span class="nn">numpy</span> <span class="k">as</span> <span class="nn">np</span>

<span class="k">def</span> <span class="nf">busca_min_cython2</span><span class="p">(</span><span class="n">malla</span><span class="p">):</span>
    <span class="k">cdef</span> <span class="kt">list</span> <span class="nf">minimosx</span><span class="p">,</span> <span class="nf">minimosy</span>
    <span class="k">cdef</span> <span class="kt">unsigned</span> <span class="kt">int</span> <span class="nf">i</span><span class="p">,</span> <span class="nf">j</span>
    <span class="k">cdef</span> <span class="kt">unsigned</span> <span class="kt">int</span> <span class="nf">ii</span> <span class="o">=</span> <span class="n">malla</span><span class="o">.</span><span class="n">shape</span><span class="p">[</span><span class="mf">1</span><span class="p">]</span><span class="o">-</span><span class="mf">1</span>
    <span class="k">cdef</span> <span class="kt">unsigned</span> <span class="kt">int</span> <span class="nf">jj</span> <span class="o">=</span> <span class="n">malla</span><span class="o">.</span><span class="n">shape</span><span class="p">[</span><span class="mf"></span><span class="p">]</span><span class="o">-</span><span class="mf">1</span>
    <span class="n">minimosx</span> <span class="o">=</span> <span class="p">[]</span>
    <span class="n">minimosy</span> <span class="o">=</span> <span class="p">[]</span>
    <span class="k">for</span> <span class="n">i</span> <span class="ow">in</span> <span class="nb">range</span><span class="p">(</span><span class="mf">1</span><span class="p">,</span> <span class="n">ii</span><span class="p">):</span>
        <span class="k">for</span> <span class="n">j</span> <span class="ow">in</span> <span class="nb">range</span><span class="p">(</span><span class="mf">1</span><span class="p">,</span> <span class="n">jj</span><span class="p">):</span>
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
          <pre><span class="o">%</span><span class="k">timeit</span> busca_min_cython2(data)
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
          <pre>1 loops, best of 3: 3.55 s per loop
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
      Vaya decepción... No hemos conseguido gran cosa, tenemos un código un poco más largo y estamos peor que en la <strong>toma 1</strong>.<br /> En realidad, estamos usando objetos Python como listas (no es un tipo C/C++ puro pero Cython lo declara como puntero a algún tipo <code>struct</code> de Python) o numpy arrays y no hemos definido las variables de entrada y de salida.<br /> [INCISO] Cuando existe un tipo Python y C que tienen el mismo nombre (por ejemplo, <code>int</code>) predomina el de C (porque es lo deseable, ¿no?).</p>
    </div>
  </div>
</div>

<div>
  <div>
  </div>
  
  <div>
    <div>
      <h1 id="Cythonizando,-que-es-gerundio-(toma-3).">
        Cythonizando, que es gerundio (toma 3).<a class="anchor-link" href="#Cythonizando,-que-es-gerundio-(toma-3).">&#182;</a>
      </h1>
    </div>
  </div>
</div>

<div>
  <div>
  </div>
  
  <div>
    <div>
      En Cython existen tres tipos de funciones, las definidas en el espacio Python con <code>def</code>, las definidas en el espacio C con <code>cdef</code> (sí, lo mismo que usamos para declarar los tipos) y las definidas en ambos espacios con <code>cpdef</code>.</p> 
      
      <ul>
        <li>
          <code>def</code>: ya lo hemos visto y funciona como se espera. Accesible desde Python
        </li>
        <li>
          <code>cdef</code>: No es accesible desde Python y la tendremos que envolver con una función Python para poder acceder a la misma.
        </li>
        <li>
          <code>cpdef</code>: Es accesible tanto desde Python como desde C y Cython se encargará de hacer el 'envoltorio' para nosotros. Esto meterá un poco más de código y empeorará levemente el rendimiento.
        </li>
      </ul>
      
      <p>
        Si definimos una función con <code>cdef</code> debería ser una función que se usa internamente dentro del módulo Cython que vayamos a crear y que no sea necesario llamar desde Python.
      </p>
    </div>
  </div>
</div>

<div>
  <div>
  </div>
  
  <div>
    <div>
      Veamos un ejemplo de lo dicho anteriormente definiendo la salida de la función como tupla:</p>
    </div>
  </div>
</div>

<div>
  <div>
    <div>
      <div>
        <div class=" highlight hl-ipython3">
          <pre><span class="o">%%</span><span class="n">cython</span> <span class="o">--</span><span class="n">name</span> <span class="n">probandocython3</span>
<span class="k">import</span> <span class="nn">numpy</span> <span class="k">as</span> <span class="nn">np</span>

<span class="k">cdef</span> <span class="kt">tuple</span> <span class="nf">cbusca_min_cython3</span><span class="p">(</span><span class="n">malla</span><span class="p">):</span>
    <span class="k">cdef</span> <span class="kt">list</span> <span class="nf">minimosx</span><span class="p">,</span> <span class="nf">minimosy</span>
    <span class="k">cdef</span> <span class="kt">unsigned</span> <span class="kt">int</span> <span class="nf">i</span><span class="p">,</span> <span class="nf">j</span>
    <span class="k">cdef</span> <span class="kt">unsigned</span> <span class="kt">int</span> <span class="nf">ii</span> <span class="o">=</span> <span class="n">malla</span><span class="o">.</span><span class="n">shape</span><span class="p">[</span><span class="mf">1</span><span class="p">]</span><span class="o">-</span><span class="mf">1</span>
    <span class="k">cdef</span> <span class="kt">unsigned</span> <span class="kt">int</span> <span class="nf">jj</span> <span class="o">=</span> <span class="n">malla</span><span class="o">.</span><span class="n">shape</span><span class="p">[</span><span class="mf"></span><span class="p">]</span><span class="o">-</span><span class="mf">1</span>
    <span class="k">cdef</span> <span class="kt">unsigned</span> <span class="kt">int</span> <span class="nf">start</span> <span class="o">=</span> <span class="mf">1</span>
    <span class="n">minimosx</span> <span class="o">=</span> <span class="p">[]</span>
    <span class="n">minimosy</span> <span class="o">=</span> <span class="p">[]</span>
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

<span class="k">def</span> <span class="nf">busca_min_cython3</span><span class="p">(</span><span class="n">malla</span><span class="p">):</span>
    <span class="k">return</span> <span class="n">cbusca_min_cython3</span><span class="p">(</span><span class="n">malla</span><span class="p">)</span>
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
          <pre><span class="o">%</span><span class="k">timeit</span> busca_min_cython3(data)
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
          <pre>1 loops, best of 3: 3.62 s per loop
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
      Vaya, seguimos sin estar muy a gusto con estos resultados.<br /> Seguimos sin definir el tipo del valor de entrada.<br /> La función mágica <code>%%cython</code> dispone de una serie de funcionalidades entre la que se encuentra <code>-a</code> o <code>--annotate</code> (además del <code>-n</code> o <code>--name</code> que ya hemos visto). Si le pasamos este parámetro podremos ver una representación del código con colores marcando las partes más lentas (amarillo más oscuro) y más optmizadas (más claro) o a la velocidad de C (blanco). Vamos a usarlo para saber donde tenemos cuellos de botella (aplicado a nuestra última versión del código):</p>
    </div>
  </div>
</div>

<div>
  <div>
    <div>
      <div>
        <div class=" highlight hl-ipython3">
          <pre><span class="o">%%</span><span class="n">cython</span> <span class="o">--</span><span class="n">annotate</span>
<span class="k">import</span> <span class="nn">numpy</span> <span class="k">as</span> <span class="nn">np</span>

<span class="k">cdef</span> <span class="kt">tuple</span> <span class="nf">cbusca_min_cython3</span><span class="p">(</span><span class="n">malla</span><span class="p">):</span>
    <span class="k">cdef</span> <span class="kt">list</span> <span class="nf">minimosx</span><span class="p">,</span> <span class="nf">minimosy</span>
    <span class="k">cdef</span> <span class="kt">unsigned</span> <span class="kt">int</span> <span class="nf">i</span><span class="p">,</span> <span class="nf">j</span>
    <span class="k">cdef</span> <span class="kt">unsigned</span> <span class="kt">int</span> <span class="nf">ii</span> <span class="o">=</span> <span class="n">malla</span><span class="o">.</span><span class="n">shape</span><span class="p">[</span><span class="mf">1</span><span class="p">]</span><span class="o">-</span><span class="mf">1</span>
    <span class="k">cdef</span> <span class="kt">unsigned</span> <span class="kt">int</span> <span class="nf">jj</span> <span class="o">=</span> <span class="n">malla</span><span class="o">.</span><span class="n">shape</span><span class="p">[</span><span class="mf"></span><span class="p">]</span><span class="o">-</span><span class="mf">1</span>
    <span class="k">cdef</span> <span class="kt">unsigned</span> <span class="kt">int</span> <span class="nf">start</span> <span class="o">=</span> <span class="mf">1</span>
    <span class="n">minimosx</span> <span class="o">=</span> <span class="p">[]</span>
    <span class="n">minimosy</span> <span class="o">=</span> <span class="p">[]</span>
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

<span class="k">def</span> <span class="nf">busca_min_cython3</span><span class="p">(</span><span class="n">malla</span><span class="p">):</span>
    <span class="k">return</span> <span class="n">cbusca_min_cython3</span><span class="p">(</span><span class="n">malla</span><span class="p">)</span>
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
        
        <p>
          [INCISO] En el código a continuación, si pulsáis sobre el símbolo '+' que está delante de cada número de línea podréis ver el código C que se genera
        </p>
        
        <div>
          <br /> <!-- Generated by Cython 0.22 -->
          
          <br /> <br /> <br /> <br /> Generated by Cython 0.22</p> 
          
          <div class="cython">
            <pre class='cython line score-8' onclick='toggleDiv(this)'>+01: <span class="k">import</span> <span class="nn">numpy</span> <span class="k">as</span> <span class="nn">np</span></pre>
            
            <pre class='cython code score-8'>  __pyx_t_1 = <span class='pyx_c_api'>__Pyx_Import</span>(__pyx_n_s_numpy, 0, -1);<span class='error_goto'> if (unlikely(!__pyx_t_1)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 1; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
  <span class='refnanny'>__Pyx_GOTREF</span>(__pyx_t_1);
  if (<span class='py_c_api'>PyDict_SetItem</span>(__pyx_d, __pyx_n_s_np, __pyx_t_1) &lt; 0) <span class='error_goto'>{__pyx_filename = __pyx_f[0]; __pyx_lineno = 1; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
  <span class='pyx_macro_api'>__Pyx_DECREF</span>(__pyx_t_1); __pyx_t_1 = 0;
</pre>
            
            <pre class='cython line score-0'>&#xA0;02: </pre>
            
            <pre class='cython line score-9' onclick='toggleDiv(this)'>+03: <span class="k">cdef</span> <span class="kt">tuple</span> <span class="nf">cbusca_min_cython3</span><span class="p">(</span><span class="n">malla</span><span class="p">):</span></pre>
            
            <pre class='cython code score-9'>static PyObject *__pyx_f_46_cython_magic_b76d9f95ffc9db5b7e97e92e04623490_cbusca_min_cython3(PyObject *__pyx_v_malla) {
  PyObject *__pyx_v_minimosx = 0;
  PyObject *__pyx_v_minimosy = 0;
  unsigned int __pyx_v_i;
  unsigned int __pyx_v_j;
  unsigned int __pyx_v_ii;
  unsigned int __pyx_v_jj;
  unsigned int __pyx_v_start;
  PyObject *__pyx_r = NULL;
  <span class='refnanny'>__Pyx_RefNannyDeclarations</span>
  <span class='refnanny'>__Pyx_RefNannySetupContext</span>("cbusca_min_cython3", 0);
/* … */
  /* function exit code */
  __pyx_L1_error:;
  <span class='pyx_macro_api'>__Pyx_XDECREF</span>(__pyx_t_1);
  <span class='pyx_macro_api'>__Pyx_XDECREF</span>(__pyx_t_2);
  <span class='pyx_macro_api'>__Pyx_XDECREF</span>(__pyx_t_8);
  <span class='pyx_macro_api'>__Pyx_XDECREF</span>(__pyx_t_9);
  <span class='pyx_macro_api'>__Pyx_XDECREF</span>(__pyx_t_12);
  <span class='pyx_c_api'>__Pyx_AddTraceback</span>("_cython_magic_b76d9f95ffc9db5b7e97e92e04623490.cbusca_min_cython3", __pyx_clineno, __pyx_lineno, __pyx_filename);
  __pyx_r = 0;
  __pyx_L0:;
  <span class='pyx_macro_api'>__Pyx_XDECREF</span>(__pyx_v_minimosx);
  <span class='pyx_macro_api'>__Pyx_XDECREF</span>(__pyx_v_minimosy);
  <span class='refnanny'>__Pyx_XGIVEREF</span>(__pyx_r);
  <span class='refnanny'>__Pyx_RefNannyFinishContext</span>();
  return __pyx_r;
}
</pre>
            
            <pre class='cython line score-0'>&#xA0;04:     <span class="k">cdef</span> <span class="kt">list</span> <span class="nf">minimosx</span><span class="p">,</span> <span class="nf">minimosy</span></pre>
            
            <pre class='cython line score-0'>&#xA0;05:     <span class="k">cdef</span> <span class="kt">unsigned</span> <span class="kt">int</span> <span class="nf">i</span><span class="p">,</span> <span class="nf">j</span></pre>
            
            <pre class='cython line score-14' onclick='toggleDiv(this)'>+06:     <span class="k">cdef</span> <span class="kt">unsigned</span> <span class="kt">int</span> <span class="nf">ii</span> <span class="o">=</span> <span class="n">malla</span><span class="o">.</span><span class="n">shape</span><span class="p">[</span><span class="mf">1</span><span class="p">]</span><span class="o">-</span><span class="mf">1</span></pre>
            
            <pre class='cython code score-14'>  __pyx_t_1 = <span class='pyx_c_api'>__Pyx_PyObject_GetAttrStr</span>(__pyx_v_malla, __pyx_n_s_shape);<span class='error_goto'> if (unlikely(!__pyx_t_1)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 6; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
  <span class='refnanny'>__Pyx_GOTREF</span>(__pyx_t_1);
  __pyx_t_2 = <span class='pyx_c_api'>__Pyx_GetItemInt</span>(__pyx_t_1, 1, long, 1, __Pyx_PyInt_From_long, 0, 0, 1);<span class='error_goto'> if (unlikely(__pyx_t_2 == NULL)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 6; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>;
  <span class='refnanny'>__Pyx_GOTREF</span>(__pyx_t_2);
  <span class='pyx_macro_api'>__Pyx_DECREF</span>(__pyx_t_1); __pyx_t_1 = 0;
  __pyx_t_1 = <span class='py_c_api'>PyNumber_Subtract</span>(__pyx_t_2, __pyx_int_1);<span class='error_goto'> if (unlikely(!__pyx_t_1)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 6; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
  <span class='refnanny'>__Pyx_GOTREF</span>(__pyx_t_1);
  <span class='pyx_macro_api'>__Pyx_DECREF</span>(__pyx_t_2); __pyx_t_2 = 0;
  __pyx_t_3 = <span class='pyx_c_api'>__Pyx_PyInt_As_unsigned_int</span>(__pyx_t_1);<span class='error_goto'> if (unlikely((__pyx_t_3 == (unsigned int)-1) && PyErr_Occurred())) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 6; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
  <span class='pyx_macro_api'>__Pyx_DECREF</span>(__pyx_t_1); __pyx_t_1 = 0;
  __pyx_v_ii = __pyx_t_3;
</pre>
            
            <pre class='cython line score-14' onclick='toggleDiv(this)'>+07:     <span class="k">cdef</span> <span class="kt">unsigned</span> <span class="kt">int</span> <span class="nf">jj</span> <span class="o">=</span> <span class="n">malla</span><span class="o">.</span><span class="n">shape</span><span class="p">[</span><span class="mf"></span><span class="p">]</span><span class="o">-</span><span class="mf">1</span></pre>
            
            <pre class='cython code score-14'>  __pyx_t_1 = <span class='pyx_c_api'>__Pyx_PyObject_GetAttrStr</span>(__pyx_v_malla, __pyx_n_s_shape);<span class='error_goto'> if (unlikely(!__pyx_t_1)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 7; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
  <span class='refnanny'>__Pyx_GOTREF</span>(__pyx_t_1);
  __pyx_t_2 = <span class='pyx_c_api'>__Pyx_GetItemInt</span>(__pyx_t_1, 0, long, 1, __Pyx_PyInt_From_long, 0, 0, 1);<span class='error_goto'> if (unlikely(__pyx_t_2 == NULL)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 7; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>;
  <span class='refnanny'>__Pyx_GOTREF</span>(__pyx_t_2);
  <span class='pyx_macro_api'>__Pyx_DECREF</span>(__pyx_t_1); __pyx_t_1 = 0;
  __pyx_t_1 = <span class='py_c_api'>PyNumber_Subtract</span>(__pyx_t_2, __pyx_int_1);<span class='error_goto'> if (unlikely(!__pyx_t_1)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 7; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
  <span class='refnanny'>__Pyx_GOTREF</span>(__pyx_t_1);
  <span class='pyx_macro_api'>__Pyx_DECREF</span>(__pyx_t_2); __pyx_t_2 = 0;
  __pyx_t_3 = <span class='pyx_c_api'>__Pyx_PyInt_As_unsigned_int</span>(__pyx_t_1);<span class='error_goto'> if (unlikely((__pyx_t_3 == (unsigned int)-1) && PyErr_Occurred())) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 7; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
  <span class='pyx_macro_api'>__Pyx_DECREF</span>(__pyx_t_1); __pyx_t_1 = 0;
  __pyx_v_jj = __pyx_t_3;
</pre>
            
            <pre class='cython line score-0' onclick='toggleDiv(this)'>+08:     <span class="k">cdef</span> <span class="kt">unsigned</span> <span class="kt">int</span> <span class="nf">start</span> <span class="o">=</span> <span class="mf">1</span></pre>
            
            <pre class='cython code score-0'>  __pyx_v_start = 1;
</pre>
            
            <pre class='cython line score-5' onclick='toggleDiv(this)'>+09:     <span class="n">minimosx</span> <span class="o">=</span> <span class="p">[]</span></pre>
            
            <pre class='cython code score-5'>  __pyx_t_1 = <span class='py_c_api'>PyList_New</span>(0);<span class='error_goto'> if (unlikely(!__pyx_t_1)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 9; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
  <span class='refnanny'>__Pyx_GOTREF</span>(__pyx_t_1);
  __pyx_v_minimosx = ((PyObject*)__pyx_t_1);
  __pyx_t_1 = 0;
</pre>
            
            <pre class='cython line score-5' onclick='toggleDiv(this)'>+10:     <span class="n">minimosy</span> <span class="o">=</span> <span class="p">[]</span></pre>
            
            <pre class='cython code score-5'>  __pyx_t_1 = <span class='py_c_api'>PyList_New</span>(0);<span class='error_goto'> if (unlikely(!__pyx_t_1)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 10; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
  <span class='refnanny'>__Pyx_GOTREF</span>(__pyx_t_1);
  __pyx_v_minimosy = ((PyObject*)__pyx_t_1);
  __pyx_t_1 = 0;
</pre>
            
            <pre class='cython line score-0' onclick='toggleDiv(this)'>+11:     <span class="k">for</span> <span class="n">i</span> <span class="ow">in</span> <span class="nb">range</span><span class="p">(</span><span class="n">start</span><span class="p">,</span> <span class="n">ii</span><span class="p">):</span></pre>
            
            <pre class='cython code score-0'>  __pyx_t_3 = __pyx_v_ii;
  for (__pyx_t_4 = __pyx_v_start; __pyx_t_4 &lt; __pyx_t_3; __pyx_t_4+=1) {
    __pyx_v_i = __pyx_t_4;
</pre>
            
            <pre class='cython line score-0' onclick='toggleDiv(this)'>+12:         <span class="k">for</span> <span class="n">j</span> <span class="ow">in</span> <span class="nb">range</span><span class="p">(</span><span class="n">start</span><span class="p">,</span> <span class="n">jj</span><span class="p">):</span></pre>
            
            <pre class='cython code score-0'>    __pyx_t_5 = __pyx_v_jj;
    for (__pyx_t_6 = __pyx_v_start; __pyx_t_6 &lt; __pyx_t_5; __pyx_t_6+=1) {
      __pyx_v_j = __pyx_t_6;
</pre>
            
            <pre class='cython line score-44' onclick='toggleDiv(this)'>+13:             <span class="k">if</span> <span class="p">(</span><span class="n">malla</span><span class="p">[</span><span class="n">j</span><span class="p">,</span> <span class="n">i</span><span class="p">]</span> <span class="o">&lt;</span> <span class="n">malla</span><span class="p">[</span><span class="n">j</span><span class="o">-</span><span class="mf">1</span><span class="p">,</span> <span class="n">i</span><span class="o">-</span><span class="mf">1</span><span class="p">]</span> <span class="ow">and</span></pre>
            
            <pre class='cython code score-44'>      __pyx_t_1 = <span class='pyx_c_api'>__Pyx_PyInt_From_unsigned_int</span>(__pyx_v_j);<span class='error_goto'> if (unlikely(!__pyx_t_1)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 13; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
      <span class='refnanny'>__Pyx_GOTREF</span>(__pyx_t_1);
      __pyx_t_2 = <span class='pyx_c_api'>__Pyx_PyInt_From_unsigned_int</span>(__pyx_v_i);<span class='error_goto'> if (unlikely(!__pyx_t_2)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 13; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
      <span class='refnanny'>__Pyx_GOTREF</span>(__pyx_t_2);
      __pyx_t_8 = <span class='py_c_api'>PyTuple_New</span>(2);<span class='error_goto'> if (unlikely(!__pyx_t_8)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 13; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
      <span class='refnanny'>__Pyx_GOTREF</span>(__pyx_t_8);
      <span class='py_macro_api'>PyTuple_SET_ITEM</span>(__pyx_t_8, 0, __pyx_t_1);
      <span class='refnanny'>__Pyx_GIVEREF</span>(__pyx_t_1);
      <span class='py_macro_api'>PyTuple_SET_ITEM</span>(__pyx_t_8, 1, __pyx_t_2);
      <span class='refnanny'>__Pyx_GIVEREF</span>(__pyx_t_2);
      __pyx_t_1 = 0;
      __pyx_t_2 = 0;
      __pyx_t_2 = <span class='py_c_api'>PyObject_GetItem</span>(__pyx_v_malla, __pyx_t_8);<span class='error_goto'> if (unlikely(__pyx_t_2 == NULL)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 13; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>;
      <span class='refnanny'>__Pyx_GOTREF</span>(__pyx_t_2);
      <span class='pyx_macro_api'>__Pyx_DECREF</span>(__pyx_t_8); __pyx_t_8 = 0;
      __pyx_t_8 = <span class='pyx_c_api'>__Pyx_PyInt_From_long</span>((__pyx_v_j - 1));<span class='error_goto'> if (unlikely(!__pyx_t_8)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 13; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
      <span class='refnanny'>__Pyx_GOTREF</span>(__pyx_t_8);
      __pyx_t_1 = <span class='pyx_c_api'>__Pyx_PyInt_From_long</span>((__pyx_v_i - 1));<span class='error_goto'> if (unlikely(!__pyx_t_1)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 13; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
      <span class='refnanny'>__Pyx_GOTREF</span>(__pyx_t_1);
      __pyx_t_9 = <span class='py_c_api'>PyTuple_New</span>(2);<span class='error_goto'> if (unlikely(!__pyx_t_9)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 13; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
      <span class='refnanny'>__Pyx_GOTREF</span>(__pyx_t_9);
      <span class='py_macro_api'>PyTuple_SET_ITEM</span>(__pyx_t_9, 0, __pyx_t_8);
      <span class='refnanny'>__Pyx_GIVEREF</span>(__pyx_t_8);
      <span class='py_macro_api'>PyTuple_SET_ITEM</span>(__pyx_t_9, 1, __pyx_t_1);
      <span class='refnanny'>__Pyx_GIVEREF</span>(__pyx_t_1);
      __pyx_t_8 = 0;
      __pyx_t_1 = 0;
      __pyx_t_1 = <span class='py_c_api'>PyObject_GetItem</span>(__pyx_v_malla, __pyx_t_9);<span class='error_goto'> if (unlikely(__pyx_t_1 == NULL)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 13; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>;
      <span class='refnanny'>__Pyx_GOTREF</span>(__pyx_t_1);
      <span class='pyx_macro_api'>__Pyx_DECREF</span>(__pyx_t_9); __pyx_t_9 = 0;
      __pyx_t_9 = <span class='py_c_api'>PyObject_RichCompare</span>(__pyx_t_2, __pyx_t_1, Py_LT); <span class='refnanny'>__Pyx_XGOTREF</span>(__pyx_t_9);<span class='error_goto'> if (unlikely(!__pyx_t_9)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 13; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
      <span class='pyx_macro_api'>__Pyx_DECREF</span>(__pyx_t_2); __pyx_t_2 = 0;
      <span class='pyx_macro_api'>__Pyx_DECREF</span>(__pyx_t_1); __pyx_t_1 = 0;
      __pyx_t_10 = <span class='pyx_c_api'>__Pyx_PyObject_IsTrue</span>(__pyx_t_9);<span class='error_goto'> if (unlikely(__pyx_t_10 &lt; 0)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 13; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
      <span class='pyx_macro_api'>__Pyx_DECREF</span>(__pyx_t_9); __pyx_t_9 = 0;
      if (__pyx_t_10) {
      } else {
        __pyx_t_7 = __pyx_t_10;
        goto __pyx_L8_bool_binop_done;
      }
</pre>
            
            <pre class='cython line score-44' onclick='toggleDiv(this)'>+14:                 <span class="n">malla</span><span class="p">[</span><span class="n">j</span><span class="p">,</span> <span class="n">i</span><span class="p">]</span> <span class="o">&lt;</span> <span class="n">malla</span><span class="p">[</span><span class="n">j</span><span class="o">-</span><span class="mf">1</span><span class="p">,</span> <span class="n">i</span><span class="p">]</span> <span class="ow">and</span></pre>
            
            <pre class='cython code score-44'>      __pyx_t_9 = <span class='pyx_c_api'>__Pyx_PyInt_From_unsigned_int</span>(__pyx_v_j);<span class='error_goto'> if (unlikely(!__pyx_t_9)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 14; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
      <span class='refnanny'>__Pyx_GOTREF</span>(__pyx_t_9);
      __pyx_t_1 = <span class='pyx_c_api'>__Pyx_PyInt_From_unsigned_int</span>(__pyx_v_i);<span class='error_goto'> if (unlikely(!__pyx_t_1)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 14; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
      <span class='refnanny'>__Pyx_GOTREF</span>(__pyx_t_1);
      __pyx_t_2 = <span class='py_c_api'>PyTuple_New</span>(2);<span class='error_goto'> if (unlikely(!__pyx_t_2)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 14; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
      <span class='refnanny'>__Pyx_GOTREF</span>(__pyx_t_2);
      <span class='py_macro_api'>PyTuple_SET_ITEM</span>(__pyx_t_2, 0, __pyx_t_9);
      <span class='refnanny'>__Pyx_GIVEREF</span>(__pyx_t_9);
      <span class='py_macro_api'>PyTuple_SET_ITEM</span>(__pyx_t_2, 1, __pyx_t_1);
      <span class='refnanny'>__Pyx_GIVEREF</span>(__pyx_t_1);
      __pyx_t_9 = 0;
      __pyx_t_1 = 0;
      __pyx_t_1 = <span class='py_c_api'>PyObject_GetItem</span>(__pyx_v_malla, __pyx_t_2);<span class='error_goto'> if (unlikely(__pyx_t_1 == NULL)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 14; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>;
      <span class='refnanny'>__Pyx_GOTREF</span>(__pyx_t_1);
      <span class='pyx_macro_api'>__Pyx_DECREF</span>(__pyx_t_2); __pyx_t_2 = 0;
      __pyx_t_2 = <span class='pyx_c_api'>__Pyx_PyInt_From_long</span>((__pyx_v_j - 1));<span class='error_goto'> if (unlikely(!__pyx_t_2)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 14; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
      <span class='refnanny'>__Pyx_GOTREF</span>(__pyx_t_2);
      __pyx_t_9 = <span class='pyx_c_api'>__Pyx_PyInt_From_unsigned_int</span>(__pyx_v_i);<span class='error_goto'> if (unlikely(!__pyx_t_9)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 14; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
      <span class='refnanny'>__Pyx_GOTREF</span>(__pyx_t_9);
      __pyx_t_8 = <span class='py_c_api'>PyTuple_New</span>(2);<span class='error_goto'> if (unlikely(!__pyx_t_8)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 14; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
      <span class='refnanny'>__Pyx_GOTREF</span>(__pyx_t_8);
      <span class='py_macro_api'>PyTuple_SET_ITEM</span>(__pyx_t_8, 0, __pyx_t_2);
      <span class='refnanny'>__Pyx_GIVEREF</span>(__pyx_t_2);
      <span class='py_macro_api'>PyTuple_SET_ITEM</span>(__pyx_t_8, 1, __pyx_t_9);
      <span class='refnanny'>__Pyx_GIVEREF</span>(__pyx_t_9);
      __pyx_t_2 = 0;
      __pyx_t_9 = 0;
      __pyx_t_9 = <span class='py_c_api'>PyObject_GetItem</span>(__pyx_v_malla, __pyx_t_8);<span class='error_goto'> if (unlikely(__pyx_t_9 == NULL)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 14; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>;
      <span class='refnanny'>__Pyx_GOTREF</span>(__pyx_t_9);
      <span class='pyx_macro_api'>__Pyx_DECREF</span>(__pyx_t_8); __pyx_t_8 = 0;
      __pyx_t_8 = <span class='py_c_api'>PyObject_RichCompare</span>(__pyx_t_1, __pyx_t_9, Py_LT); <span class='refnanny'>__Pyx_XGOTREF</span>(__pyx_t_8);<span class='error_goto'> if (unlikely(!__pyx_t_8)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 14; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
      <span class='pyx_macro_api'>__Pyx_DECREF</span>(__pyx_t_1); __pyx_t_1 = 0;
      <span class='pyx_macro_api'>__Pyx_DECREF</span>(__pyx_t_9); __pyx_t_9 = 0;
      __pyx_t_10 = <span class='pyx_c_api'>__Pyx_PyObject_IsTrue</span>(__pyx_t_8);<span class='error_goto'> if (unlikely(__pyx_t_10 &lt; 0)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 14; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
      <span class='pyx_macro_api'>__Pyx_DECREF</span>(__pyx_t_8); __pyx_t_8 = 0;
      if (__pyx_t_10) {
      } else {
        __pyx_t_7 = __pyx_t_10;
        goto __pyx_L8_bool_binop_done;
      }
</pre>
            
            <pre class='cython line score-44' onclick='toggleDiv(this)'>+15:                 <span class="n">malla</span><span class="p">[</span><span class="n">j</span><span class="p">,</span> <span class="n">i</span><span class="p">]</span> <span class="o">&lt;</span> <span class="n">malla</span><span class="p">[</span><span class="n">j</span><span class="o">-</span><span class="mf">1</span><span class="p">,</span> <span class="n">i</span><span class="o">+</span><span class="mf">1</span><span class="p">]</span> <span class="ow">and</span></pre>
            
            <pre class='cython code score-44'>      __pyx_t_8 = <span class='pyx_c_api'>__Pyx_PyInt_From_unsigned_int</span>(__pyx_v_j);<span class='error_goto'> if (unlikely(!__pyx_t_8)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 15; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
      <span class='refnanny'>__Pyx_GOTREF</span>(__pyx_t_8);
      __pyx_t_9 = <span class='pyx_c_api'>__Pyx_PyInt_From_unsigned_int</span>(__pyx_v_i);<span class='error_goto'> if (unlikely(!__pyx_t_9)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 15; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
      <span class='refnanny'>__Pyx_GOTREF</span>(__pyx_t_9);
      __pyx_t_1 = <span class='py_c_api'>PyTuple_New</span>(2);<span class='error_goto'> if (unlikely(!__pyx_t_1)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 15; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
      <span class='refnanny'>__Pyx_GOTREF</span>(__pyx_t_1);
      <span class='py_macro_api'>PyTuple_SET_ITEM</span>(__pyx_t_1, 0, __pyx_t_8);
      <span class='refnanny'>__Pyx_GIVEREF</span>(__pyx_t_8);
      <span class='py_macro_api'>PyTuple_SET_ITEM</span>(__pyx_t_1, 1, __pyx_t_9);
      <span class='refnanny'>__Pyx_GIVEREF</span>(__pyx_t_9);
      __pyx_t_8 = 0;
      __pyx_t_9 = 0;
      __pyx_t_9 = <span class='py_c_api'>PyObject_GetItem</span>(__pyx_v_malla, __pyx_t_1);<span class='error_goto'> if (unlikely(__pyx_t_9 == NULL)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 15; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>;
      <span class='refnanny'>__Pyx_GOTREF</span>(__pyx_t_9);
      <span class='pyx_macro_api'>__Pyx_DECREF</span>(__pyx_t_1); __pyx_t_1 = 0;
      __pyx_t_1 = <span class='pyx_c_api'>__Pyx_PyInt_From_long</span>((__pyx_v_j - 1));<span class='error_goto'> if (unlikely(!__pyx_t_1)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 15; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
      <span class='refnanny'>__Pyx_GOTREF</span>(__pyx_t_1);
      __pyx_t_8 = <span class='pyx_c_api'>__Pyx_PyInt_From_long</span>((__pyx_v_i + 1));<span class='error_goto'> if (unlikely(!__pyx_t_8)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 15; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
      <span class='refnanny'>__Pyx_GOTREF</span>(__pyx_t_8);
      __pyx_t_2 = <span class='py_c_api'>PyTuple_New</span>(2);<span class='error_goto'> if (unlikely(!__pyx_t_2)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 15; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
      <span class='refnanny'>__Pyx_GOTREF</span>(__pyx_t_2);
      <span class='py_macro_api'>PyTuple_SET_ITEM</span>(__pyx_t_2, 0, __pyx_t_1);
      <span class='refnanny'>__Pyx_GIVEREF</span>(__pyx_t_1);
      <span class='py_macro_api'>PyTuple_SET_ITEM</span>(__pyx_t_2, 1, __pyx_t_8);
      <span class='refnanny'>__Pyx_GIVEREF</span>(__pyx_t_8);
      __pyx_t_1 = 0;
      __pyx_t_8 = 0;
      __pyx_t_8 = <span class='py_c_api'>PyObject_GetItem</span>(__pyx_v_malla, __pyx_t_2);<span class='error_goto'> if (unlikely(__pyx_t_8 == NULL)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 15; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>;
      <span class='refnanny'>__Pyx_GOTREF</span>(__pyx_t_8);
      <span class='pyx_macro_api'>__Pyx_DECREF</span>(__pyx_t_2); __pyx_t_2 = 0;
      __pyx_t_2 = <span class='py_c_api'>PyObject_RichCompare</span>(__pyx_t_9, __pyx_t_8, Py_LT); <span class='refnanny'>__Pyx_XGOTREF</span>(__pyx_t_2);<span class='error_goto'> if (unlikely(!__pyx_t_2)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 15; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
      <span class='pyx_macro_api'>__Pyx_DECREF</span>(__pyx_t_9); __pyx_t_9 = 0;
      <span class='pyx_macro_api'>__Pyx_DECREF</span>(__pyx_t_8); __pyx_t_8 = 0;
      __pyx_t_10 = <span class='pyx_c_api'>__Pyx_PyObject_IsTrue</span>(__pyx_t_2);<span class='error_goto'> if (unlikely(__pyx_t_10 &lt; 0)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 15; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
      <span class='pyx_macro_api'>__Pyx_DECREF</span>(__pyx_t_2); __pyx_t_2 = 0;
      if (__pyx_t_10) {
      } else {
        __pyx_t_7 = __pyx_t_10;
        goto __pyx_L8_bool_binop_done;
      }
</pre>
            
            <pre class='cython line score-44' onclick='toggleDiv(this)'>+16:                 <span class="n">malla</span><span class="p">[</span><span class="n">j</span><span class="p">,</span> <span class="n">i</span><span class="p">]</span> <span class="o">&lt;</span> <span class="n">malla</span><span class="p">[</span><span class="n">j</span><span class="p">,</span> <span class="n">i</span><span class="o">-</span><span class="mf">1</span><span class="p">]</span> <span class="ow">and</span></pre>
            
            <pre class='cython code score-44'>      __pyx_t_2 = <span class='pyx_c_api'>__Pyx_PyInt_From_unsigned_int</span>(__pyx_v_j);<span class='error_goto'> if (unlikely(!__pyx_t_2)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 16; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
      <span class='refnanny'>__Pyx_GOTREF</span>(__pyx_t_2);
      __pyx_t_8 = <span class='pyx_c_api'>__Pyx_PyInt_From_unsigned_int</span>(__pyx_v_i);<span class='error_goto'> if (unlikely(!__pyx_t_8)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 16; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
      <span class='refnanny'>__Pyx_GOTREF</span>(__pyx_t_8);
      __pyx_t_9 = <span class='py_c_api'>PyTuple_New</span>(2);<span class='error_goto'> if (unlikely(!__pyx_t_9)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 16; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
      <span class='refnanny'>__Pyx_GOTREF</span>(__pyx_t_9);
      <span class='py_macro_api'>PyTuple_SET_ITEM</span>(__pyx_t_9, 0, __pyx_t_2);
      <span class='refnanny'>__Pyx_GIVEREF</span>(__pyx_t_2);
      <span class='py_macro_api'>PyTuple_SET_ITEM</span>(__pyx_t_9, 1, __pyx_t_8);
      <span class='refnanny'>__Pyx_GIVEREF</span>(__pyx_t_8);
      __pyx_t_2 = 0;
      __pyx_t_8 = 0;
      __pyx_t_8 = <span class='py_c_api'>PyObject_GetItem</span>(__pyx_v_malla, __pyx_t_9);<span class='error_goto'> if (unlikely(__pyx_t_8 == NULL)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 16; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>;
      <span class='refnanny'>__Pyx_GOTREF</span>(__pyx_t_8);
      <span class='pyx_macro_api'>__Pyx_DECREF</span>(__pyx_t_9); __pyx_t_9 = 0;
      __pyx_t_9 = <span class='pyx_c_api'>__Pyx_PyInt_From_unsigned_int</span>(__pyx_v_j);<span class='error_goto'> if (unlikely(!__pyx_t_9)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 16; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
      <span class='refnanny'>__Pyx_GOTREF</span>(__pyx_t_9);
      __pyx_t_2 = <span class='pyx_c_api'>__Pyx_PyInt_From_long</span>((__pyx_v_i - 1));<span class='error_goto'> if (unlikely(!__pyx_t_2)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 16; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
      <span class='refnanny'>__Pyx_GOTREF</span>(__pyx_t_2);
      __pyx_t_1 = <span class='py_c_api'>PyTuple_New</span>(2);<span class='error_goto'> if (unlikely(!__pyx_t_1)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 16; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
      <span class='refnanny'>__Pyx_GOTREF</span>(__pyx_t_1);
      <span class='py_macro_api'>PyTuple_SET_ITEM</span>(__pyx_t_1, 0, __pyx_t_9);
      <span class='refnanny'>__Pyx_GIVEREF</span>(__pyx_t_9);
      <span class='py_macro_api'>PyTuple_SET_ITEM</span>(__pyx_t_1, 1, __pyx_t_2);
      <span class='refnanny'>__Pyx_GIVEREF</span>(__pyx_t_2);
      __pyx_t_9 = 0;
      __pyx_t_2 = 0;
      __pyx_t_2 = <span class='py_c_api'>PyObject_GetItem</span>(__pyx_v_malla, __pyx_t_1);<span class='error_goto'> if (unlikely(__pyx_t_2 == NULL)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 16; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>;
      <span class='refnanny'>__Pyx_GOTREF</span>(__pyx_t_2);
      <span class='pyx_macro_api'>__Pyx_DECREF</span>(__pyx_t_1); __pyx_t_1 = 0;
      __pyx_t_1 = <span class='py_c_api'>PyObject_RichCompare</span>(__pyx_t_8, __pyx_t_2, Py_LT); <span class='refnanny'>__Pyx_XGOTREF</span>(__pyx_t_1);<span class='error_goto'> if (unlikely(!__pyx_t_1)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 16; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
      <span class='pyx_macro_api'>__Pyx_DECREF</span>(__pyx_t_8); __pyx_t_8 = 0;
      <span class='pyx_macro_api'>__Pyx_DECREF</span>(__pyx_t_2); __pyx_t_2 = 0;
      __pyx_t_10 = <span class='pyx_c_api'>__Pyx_PyObject_IsTrue</span>(__pyx_t_1);<span class='error_goto'> if (unlikely(__pyx_t_10 &lt; 0)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 16; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
      <span class='pyx_macro_api'>__Pyx_DECREF</span>(__pyx_t_1); __pyx_t_1 = 0;
      if (__pyx_t_10) {
      } else {
        __pyx_t_7 = __pyx_t_10;
        goto __pyx_L8_bool_binop_done;
      }
</pre>
            
            <pre class='cython line score-44' onclick='toggleDiv(this)'>+17:                 <span class="n">malla</span><span class="p">[</span><span class="n">j</span><span class="p">,</span> <span class="n">i</span><span class="p">]</span> <span class="o">&lt;</span> <span class="n">malla</span><span class="p">[</span><span class="n">j</span><span class="p">,</span> <span class="n">i</span><span class="o">+</span><span class="mf">1</span><span class="p">]</span> <span class="ow">and</span></pre>
            
            <pre class='cython code score-44'>      __pyx_t_1 = <span class='pyx_c_api'>__Pyx_PyInt_From_unsigned_int</span>(__pyx_v_j);<span class='error_goto'> if (unlikely(!__pyx_t_1)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 17; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
      <span class='refnanny'>__Pyx_GOTREF</span>(__pyx_t_1);
      __pyx_t_2 = <span class='pyx_c_api'>__Pyx_PyInt_From_unsigned_int</span>(__pyx_v_i);<span class='error_goto'> if (unlikely(!__pyx_t_2)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 17; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
      <span class='refnanny'>__Pyx_GOTREF</span>(__pyx_t_2);
      __pyx_t_8 = <span class='py_c_api'>PyTuple_New</span>(2);<span class='error_goto'> if (unlikely(!__pyx_t_8)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 17; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
      <span class='refnanny'>__Pyx_GOTREF</span>(__pyx_t_8);
      <span class='py_macro_api'>PyTuple_SET_ITEM</span>(__pyx_t_8, 0, __pyx_t_1);
      <span class='refnanny'>__Pyx_GIVEREF</span>(__pyx_t_1);
      <span class='py_macro_api'>PyTuple_SET_ITEM</span>(__pyx_t_8, 1, __pyx_t_2);
      <span class='refnanny'>__Pyx_GIVEREF</span>(__pyx_t_2);
      __pyx_t_1 = 0;
      __pyx_t_2 = 0;
      __pyx_t_2 = <span class='py_c_api'>PyObject_GetItem</span>(__pyx_v_malla, __pyx_t_8);<span class='error_goto'> if (unlikely(__pyx_t_2 == NULL)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 17; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>;
      <span class='refnanny'>__Pyx_GOTREF</span>(__pyx_t_2);
      <span class='pyx_macro_api'>__Pyx_DECREF</span>(__pyx_t_8); __pyx_t_8 = 0;
      __pyx_t_8 = <span class='pyx_c_api'>__Pyx_PyInt_From_unsigned_int</span>(__pyx_v_j);<span class='error_goto'> if (unlikely(!__pyx_t_8)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 17; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
      <span class='refnanny'>__Pyx_GOTREF</span>(__pyx_t_8);
      __pyx_t_1 = <span class='pyx_c_api'>__Pyx_PyInt_From_long</span>((__pyx_v_i + 1));<span class='error_goto'> if (unlikely(!__pyx_t_1)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 17; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
      <span class='refnanny'>__Pyx_GOTREF</span>(__pyx_t_1);
      __pyx_t_9 = <span class='py_c_api'>PyTuple_New</span>(2);<span class='error_goto'> if (unlikely(!__pyx_t_9)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 17; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
      <span class='refnanny'>__Pyx_GOTREF</span>(__pyx_t_9);
      <span class='py_macro_api'>PyTuple_SET_ITEM</span>(__pyx_t_9, 0, __pyx_t_8);
      <span class='refnanny'>__Pyx_GIVEREF</span>(__pyx_t_8);
      <span class='py_macro_api'>PyTuple_SET_ITEM</span>(__pyx_t_9, 1, __pyx_t_1);
      <span class='refnanny'>__Pyx_GIVEREF</span>(__pyx_t_1);
      __pyx_t_8 = 0;
      __pyx_t_1 = 0;
      __pyx_t_1 = <span class='py_c_api'>PyObject_GetItem</span>(__pyx_v_malla, __pyx_t_9);<span class='error_goto'> if (unlikely(__pyx_t_1 == NULL)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 17; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>;
      <span class='refnanny'>__Pyx_GOTREF</span>(__pyx_t_1);
      <span class='pyx_macro_api'>__Pyx_DECREF</span>(__pyx_t_9); __pyx_t_9 = 0;
      __pyx_t_9 = <span class='py_c_api'>PyObject_RichCompare</span>(__pyx_t_2, __pyx_t_1, Py_LT); <span class='refnanny'>__Pyx_XGOTREF</span>(__pyx_t_9);<span class='error_goto'> if (unlikely(!__pyx_t_9)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 17; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
      <span class='pyx_macro_api'>__Pyx_DECREF</span>(__pyx_t_2); __pyx_t_2 = 0;
      <span class='pyx_macro_api'>__Pyx_DECREF</span>(__pyx_t_1); __pyx_t_1 = 0;
      __pyx_t_10 = <span class='pyx_c_api'>__Pyx_PyObject_IsTrue</span>(__pyx_t_9);<span class='error_goto'> if (unlikely(__pyx_t_10 &lt; 0)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 17; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
      <span class='pyx_macro_api'>__Pyx_DECREF</span>(__pyx_t_9); __pyx_t_9 = 0;
      if (__pyx_t_10) {
      } else {
        __pyx_t_7 = __pyx_t_10;
        goto __pyx_L8_bool_binop_done;
      }
</pre>
            
            <pre class='cython line score-44' onclick='toggleDiv(this)'>+18:                 <span class="n">malla</span><span class="p">[</span><span class="n">j</span><span class="p">,</span> <span class="n">i</span><span class="p">]</span> <span class="o">&lt;</span> <span class="n">malla</span><span class="p">[</span><span class="n">j</span><span class="o">+</span><span class="mf">1</span><span class="p">,</span> <span class="n">i</span><span class="o">-</span><span class="mf">1</span><span class="p">]</span> <span class="ow">and</span></pre>
            
            <pre class='cython code score-44'>      __pyx_t_9 = <span class='pyx_c_api'>__Pyx_PyInt_From_unsigned_int</span>(__pyx_v_j);<span class='error_goto'> if (unlikely(!__pyx_t_9)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 18; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
      <span class='refnanny'>__Pyx_GOTREF</span>(__pyx_t_9);
      __pyx_t_1 = <span class='pyx_c_api'>__Pyx_PyInt_From_unsigned_int</span>(__pyx_v_i);<span class='error_goto'> if (unlikely(!__pyx_t_1)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 18; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
      <span class='refnanny'>__Pyx_GOTREF</span>(__pyx_t_1);
      __pyx_t_2 = <span class='py_c_api'>PyTuple_New</span>(2);<span class='error_goto'> if (unlikely(!__pyx_t_2)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 18; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
      <span class='refnanny'>__Pyx_GOTREF</span>(__pyx_t_2);
      <span class='py_macro_api'>PyTuple_SET_ITEM</span>(__pyx_t_2, 0, __pyx_t_9);
      <span class='refnanny'>__Pyx_GIVEREF</span>(__pyx_t_9);
      <span class='py_macro_api'>PyTuple_SET_ITEM</span>(__pyx_t_2, 1, __pyx_t_1);
      <span class='refnanny'>__Pyx_GIVEREF</span>(__pyx_t_1);
      __pyx_t_9 = 0;
      __pyx_t_1 = 0;
      __pyx_t_1 = <span class='py_c_api'>PyObject_GetItem</span>(__pyx_v_malla, __pyx_t_2);<span class='error_goto'> if (unlikely(__pyx_t_1 == NULL)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 18; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>;
      <span class='refnanny'>__Pyx_GOTREF</span>(__pyx_t_1);
      <span class='pyx_macro_api'>__Pyx_DECREF</span>(__pyx_t_2); __pyx_t_2 = 0;
      __pyx_t_2 = <span class='pyx_c_api'>__Pyx_PyInt_From_long</span>((__pyx_v_j + 1));<span class='error_goto'> if (unlikely(!__pyx_t_2)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 18; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
      <span class='refnanny'>__Pyx_GOTREF</span>(__pyx_t_2);
      __pyx_t_9 = <span class='pyx_c_api'>__Pyx_PyInt_From_long</span>((__pyx_v_i - 1));<span class='error_goto'> if (unlikely(!__pyx_t_9)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 18; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
      <span class='refnanny'>__Pyx_GOTREF</span>(__pyx_t_9);
      __pyx_t_8 = <span class='py_c_api'>PyTuple_New</span>(2);<span class='error_goto'> if (unlikely(!__pyx_t_8)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 18; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
      <span class='refnanny'>__Pyx_GOTREF</span>(__pyx_t_8);
      <span class='py_macro_api'>PyTuple_SET_ITEM</span>(__pyx_t_8, 0, __pyx_t_2);
      <span class='refnanny'>__Pyx_GIVEREF</span>(__pyx_t_2);
      <span class='py_macro_api'>PyTuple_SET_ITEM</span>(__pyx_t_8, 1, __pyx_t_9);
      <span class='refnanny'>__Pyx_GIVEREF</span>(__pyx_t_9);
      __pyx_t_2 = 0;
      __pyx_t_9 = 0;
      __pyx_t_9 = <span class='py_c_api'>PyObject_GetItem</span>(__pyx_v_malla, __pyx_t_8);<span class='error_goto'> if (unlikely(__pyx_t_9 == NULL)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 18; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>;
      <span class='refnanny'>__Pyx_GOTREF</span>(__pyx_t_9);
      <span class='pyx_macro_api'>__Pyx_DECREF</span>(__pyx_t_8); __pyx_t_8 = 0;
      __pyx_t_8 = <span class='py_c_api'>PyObject_RichCompare</span>(__pyx_t_1, __pyx_t_9, Py_LT); <span class='refnanny'>__Pyx_XGOTREF</span>(__pyx_t_8);<span class='error_goto'> if (unlikely(!__pyx_t_8)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 18; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
      <span class='pyx_macro_api'>__Pyx_DECREF</span>(__pyx_t_1); __pyx_t_1 = 0;
      <span class='pyx_macro_api'>__Pyx_DECREF</span>(__pyx_t_9); __pyx_t_9 = 0;
      __pyx_t_10 = <span class='pyx_c_api'>__Pyx_PyObject_IsTrue</span>(__pyx_t_8);<span class='error_goto'> if (unlikely(__pyx_t_10 &lt; 0)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 18; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
      <span class='pyx_macro_api'>__Pyx_DECREF</span>(__pyx_t_8); __pyx_t_8 = 0;
      if (__pyx_t_10) {
      } else {
        __pyx_t_7 = __pyx_t_10;
        goto __pyx_L8_bool_binop_done;
      }
</pre>
            
            <pre class='cython line score-44' onclick='toggleDiv(this)'>+19:                 <span class="n">malla</span><span class="p">[</span><span class="n">j</span><span class="p">,</span> <span class="n">i</span><span class="p">]</span> <span class="o">&lt;</span> <span class="n">malla</span><span class="p">[</span><span class="n">j</span><span class="o">+</span><span class="mf">1</span><span class="p">,</span> <span class="n">i</span><span class="p">]</span> <span class="ow">and</span></pre>
            
            <pre class='cython code score-44'>      __pyx_t_8 = <span class='pyx_c_api'>__Pyx_PyInt_From_unsigned_int</span>(__pyx_v_j);<span class='error_goto'> if (unlikely(!__pyx_t_8)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 19; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
      <span class='refnanny'>__Pyx_GOTREF</span>(__pyx_t_8);
      __pyx_t_9 = <span class='pyx_c_api'>__Pyx_PyInt_From_unsigned_int</span>(__pyx_v_i);<span class='error_goto'> if (unlikely(!__pyx_t_9)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 19; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
      <span class='refnanny'>__Pyx_GOTREF</span>(__pyx_t_9);
      __pyx_t_1 = <span class='py_c_api'>PyTuple_New</span>(2);<span class='error_goto'> if (unlikely(!__pyx_t_1)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 19; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
      <span class='refnanny'>__Pyx_GOTREF</span>(__pyx_t_1);
      <span class='py_macro_api'>PyTuple_SET_ITEM</span>(__pyx_t_1, 0, __pyx_t_8);
      <span class='refnanny'>__Pyx_GIVEREF</span>(__pyx_t_8);
      <span class='py_macro_api'>PyTuple_SET_ITEM</span>(__pyx_t_1, 1, __pyx_t_9);
      <span class='refnanny'>__Pyx_GIVEREF</span>(__pyx_t_9);
      __pyx_t_8 = 0;
      __pyx_t_9 = 0;
      __pyx_t_9 = <span class='py_c_api'>PyObject_GetItem</span>(__pyx_v_malla, __pyx_t_1);<span class='error_goto'> if (unlikely(__pyx_t_9 == NULL)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 19; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>;
      <span class='refnanny'>__Pyx_GOTREF</span>(__pyx_t_9);
      <span class='pyx_macro_api'>__Pyx_DECREF</span>(__pyx_t_1); __pyx_t_1 = 0;
      __pyx_t_1 = <span class='pyx_c_api'>__Pyx_PyInt_From_long</span>((__pyx_v_j + 1));<span class='error_goto'> if (unlikely(!__pyx_t_1)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 19; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
      <span class='refnanny'>__Pyx_GOTREF</span>(__pyx_t_1);
      __pyx_t_8 = <span class='pyx_c_api'>__Pyx_PyInt_From_unsigned_int</span>(__pyx_v_i);<span class='error_goto'> if (unlikely(!__pyx_t_8)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 19; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
      <span class='refnanny'>__Pyx_GOTREF</span>(__pyx_t_8);
      __pyx_t_2 = <span class='py_c_api'>PyTuple_New</span>(2);<span class='error_goto'> if (unlikely(!__pyx_t_2)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 19; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
      <span class='refnanny'>__Pyx_GOTREF</span>(__pyx_t_2);
      <span class='py_macro_api'>PyTuple_SET_ITEM</span>(__pyx_t_2, 0, __pyx_t_1);
      <span class='refnanny'>__Pyx_GIVEREF</span>(__pyx_t_1);
      <span class='py_macro_api'>PyTuple_SET_ITEM</span>(__pyx_t_2, 1, __pyx_t_8);
      <span class='refnanny'>__Pyx_GIVEREF</span>(__pyx_t_8);
      __pyx_t_1 = 0;
      __pyx_t_8 = 0;
      __pyx_t_8 = <span class='py_c_api'>PyObject_GetItem</span>(__pyx_v_malla, __pyx_t_2);<span class='error_goto'> if (unlikely(__pyx_t_8 == NULL)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 19; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>;
      <span class='refnanny'>__Pyx_GOTREF</span>(__pyx_t_8);
      <span class='pyx_macro_api'>__Pyx_DECREF</span>(__pyx_t_2); __pyx_t_2 = 0;
      __pyx_t_2 = <span class='py_c_api'>PyObject_RichCompare</span>(__pyx_t_9, __pyx_t_8, Py_LT); <span class='refnanny'>__Pyx_XGOTREF</span>(__pyx_t_2);<span class='error_goto'> if (unlikely(!__pyx_t_2)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 19; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
      <span class='pyx_macro_api'>__Pyx_DECREF</span>(__pyx_t_9); __pyx_t_9 = 0;
      <span class='pyx_macro_api'>__Pyx_DECREF</span>(__pyx_t_8); __pyx_t_8 = 0;
      __pyx_t_10 = <span class='pyx_c_api'>__Pyx_PyObject_IsTrue</span>(__pyx_t_2);<span class='error_goto'> if (unlikely(__pyx_t_10 &lt; 0)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 19; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
      <span class='pyx_macro_api'>__Pyx_DECREF</span>(__pyx_t_2); __pyx_t_2 = 0;
      if (__pyx_t_10) {
      } else {
        __pyx_t_7 = __pyx_t_10;
        goto __pyx_L8_bool_binop_done;
      }
</pre>
            
            <pre class='cython line score-44' onclick='toggleDiv(this)'>+20:                 <span class="n">malla</span><span class="p">[</span><span class="n">j</span><span class="p">,</span> <span class="n">i</span><span class="p">]</span> <span class="o">&lt;</span> <span class="n">malla</span><span class="p">[</span><span class="n">j</span><span class="o">+</span><span class="mf">1</span><span class="p">,</span> <span class="n">i</span><span class="o">+</span><span class="mf">1</span><span class="p">]):</span></pre>
            
            <pre class='cython code score-44'>      __pyx_t_2 = <span class='pyx_c_api'>__Pyx_PyInt_From_unsigned_int</span>(__pyx_v_j);<span class='error_goto'> if (unlikely(!__pyx_t_2)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 20; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
      <span class='refnanny'>__Pyx_GOTREF</span>(__pyx_t_2);
      __pyx_t_8 = <span class='pyx_c_api'>__Pyx_PyInt_From_unsigned_int</span>(__pyx_v_i);<span class='error_goto'> if (unlikely(!__pyx_t_8)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 20; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
      <span class='refnanny'>__Pyx_GOTREF</span>(__pyx_t_8);
      __pyx_t_9 = <span class='py_c_api'>PyTuple_New</span>(2);<span class='error_goto'> if (unlikely(!__pyx_t_9)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 20; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
      <span class='refnanny'>__Pyx_GOTREF</span>(__pyx_t_9);
      <span class='py_macro_api'>PyTuple_SET_ITEM</span>(__pyx_t_9, 0, __pyx_t_2);
      <span class='refnanny'>__Pyx_GIVEREF</span>(__pyx_t_2);
      <span class='py_macro_api'>PyTuple_SET_ITEM</span>(__pyx_t_9, 1, __pyx_t_8);
      <span class='refnanny'>__Pyx_GIVEREF</span>(__pyx_t_8);
      __pyx_t_2 = 0;
      __pyx_t_8 = 0;
      __pyx_t_8 = <span class='py_c_api'>PyObject_GetItem</span>(__pyx_v_malla, __pyx_t_9);<span class='error_goto'> if (unlikely(__pyx_t_8 == NULL)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 20; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>;
      <span class='refnanny'>__Pyx_GOTREF</span>(__pyx_t_8);
      <span class='pyx_macro_api'>__Pyx_DECREF</span>(__pyx_t_9); __pyx_t_9 = 0;
      __pyx_t_9 = <span class='pyx_c_api'>__Pyx_PyInt_From_long</span>((__pyx_v_j + 1));<span class='error_goto'> if (unlikely(!__pyx_t_9)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 20; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
      <span class='refnanny'>__Pyx_GOTREF</span>(__pyx_t_9);
      __pyx_t_2 = <span class='pyx_c_api'>__Pyx_PyInt_From_long</span>((__pyx_v_i + 1));<span class='error_goto'> if (unlikely(!__pyx_t_2)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 20; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
      <span class='refnanny'>__Pyx_GOTREF</span>(__pyx_t_2);
      __pyx_t_1 = <span class='py_c_api'>PyTuple_New</span>(2);<span class='error_goto'> if (unlikely(!__pyx_t_1)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 20; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
      <span class='refnanny'>__Pyx_GOTREF</span>(__pyx_t_1);
      <span class='py_macro_api'>PyTuple_SET_ITEM</span>(__pyx_t_1, 0, __pyx_t_9);
      <span class='refnanny'>__Pyx_GIVEREF</span>(__pyx_t_9);
      <span class='py_macro_api'>PyTuple_SET_ITEM</span>(__pyx_t_1, 1, __pyx_t_2);
      <span class='refnanny'>__Pyx_GIVEREF</span>(__pyx_t_2);
      __pyx_t_9 = 0;
      __pyx_t_2 = 0;
      __pyx_t_2 = <span class='py_c_api'>PyObject_GetItem</span>(__pyx_v_malla, __pyx_t_1);<span class='error_goto'> if (unlikely(__pyx_t_2 == NULL)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 20; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>;
      <span class='refnanny'>__Pyx_GOTREF</span>(__pyx_t_2);
      <span class='pyx_macro_api'>__Pyx_DECREF</span>(__pyx_t_1); __pyx_t_1 = 0;
      __pyx_t_1 = <span class='py_c_api'>PyObject_RichCompare</span>(__pyx_t_8, __pyx_t_2, Py_LT); <span class='refnanny'>__Pyx_XGOTREF</span>(__pyx_t_1);<span class='error_goto'> if (unlikely(!__pyx_t_1)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 20; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
      <span class='pyx_macro_api'>__Pyx_DECREF</span>(__pyx_t_8); __pyx_t_8 = 0;
      <span class='pyx_macro_api'>__Pyx_DECREF</span>(__pyx_t_2); __pyx_t_2 = 0;
      __pyx_t_10 = <span class='pyx_c_api'>__Pyx_PyObject_IsTrue</span>(__pyx_t_1);<span class='error_goto'> if (unlikely(__pyx_t_10 &lt; 0)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 20; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
      <span class='pyx_macro_api'>__Pyx_DECREF</span>(__pyx_t_1); __pyx_t_1 = 0;
      __pyx_t_7 = __pyx_t_10;
      __pyx_L8_bool_binop_done:;
      if (__pyx_t_7) {
</pre>
            
            <pre class='cython line score-5' onclick='toggleDiv(this)'>+21:                 <span class="n">minimosx</span><span class="o">.</span><span class="n">append</span><span class="p">(</span><span class="n">i</span><span class="p">)</span></pre>
            
            <pre class='cython code score-5'>        __pyx_t_1 = <span class='pyx_c_api'>__Pyx_PyInt_From_unsigned_int</span>(__pyx_v_i);<span class='error_goto'> if (unlikely(!__pyx_t_1)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 21; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
        <span class='refnanny'>__Pyx_GOTREF</span>(__pyx_t_1);
        __pyx_t_11 = <span class='pyx_c_api'>__Pyx_PyList_Append</span>(__pyx_v_minimosx, __pyx_t_1);<span class='error_goto'> if (unlikely(__pyx_t_11 == -1)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 21; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
        <span class='pyx_macro_api'>__Pyx_DECREF</span>(__pyx_t_1); __pyx_t_1 = 0;
</pre>
            
            <pre class='cython line score-5' onclick='toggleDiv(this)'>+22:                 <span class="n">minimosy</span><span class="o">.</span><span class="n">append</span><span class="p">(</span><span class="n">j</span><span class="p">)</span></pre>
            
            <pre class='cython code score-5'>        __pyx_t_1 = <span class='pyx_c_api'>__Pyx_PyInt_From_unsigned_int</span>(__pyx_v_j);<span class='error_goto'> if (unlikely(!__pyx_t_1)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 22; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
        <span class='refnanny'>__Pyx_GOTREF</span>(__pyx_t_1);
        __pyx_t_11 = <span class='pyx_c_api'>__Pyx_PyList_Append</span>(__pyx_v_minimosy, __pyx_t_1);<span class='error_goto'> if (unlikely(__pyx_t_11 == -1)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 22; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
        <span class='pyx_macro_api'>__Pyx_DECREF</span>(__pyx_t_1); __pyx_t_1 = 0;
        goto __pyx_L7;
      }
      __pyx_L7:;
    }
  }
</pre>
            
            <pre class='cython line score-0'>&#xA0;23: </pre>
            
            <pre class='cython line score-66' onclick='toggleDiv(this)'>+24:     <span class="k">return</span> <span class="n">np</span><span class="o">.</span><span class="n">array</span><span class="p">(</span><span class="n">minimosx</span><span class="p">),</span> <span class="n">np</span><span class="o">.</span><span class="n">array</span><span class="p">(</span><span class="n">minimosy</span><span class="p">)</span></pre>
            
            <pre class='cython code score-66'>  <span class='pyx_macro_api'>__Pyx_XDECREF</span>(__pyx_r);
  __pyx_t_2 = <span class='pyx_c_api'>__Pyx_GetModuleGlobalName</span>(__pyx_n_s_np);<span class='error_goto'> if (unlikely(!__pyx_t_2)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 24; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
  <span class='refnanny'>__Pyx_GOTREF</span>(__pyx_t_2);
  __pyx_t_8 = <span class='pyx_c_api'>__Pyx_PyObject_GetAttrStr</span>(__pyx_t_2, __pyx_n_s_array);<span class='error_goto'> if (unlikely(!__pyx_t_8)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 24; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
  <span class='refnanny'>__Pyx_GOTREF</span>(__pyx_t_8);
  <span class='pyx_macro_api'>__Pyx_DECREF</span>(__pyx_t_2); __pyx_t_2 = 0;
  __pyx_t_2 = NULL;
  if (CYTHON_COMPILING_IN_CPYTHON && unlikely(<span class='py_c_api'>PyMethod_Check</span>(__pyx_t_8))) {
    __pyx_t_2 = <span class='py_macro_api'>PyMethod_GET_SELF</span>(__pyx_t_8);
    if (likely(__pyx_t_2)) {
      PyObject* function = <span class='py_macro_api'>PyMethod_GET_FUNCTION</span>(__pyx_t_8);
      <span class='pyx_macro_api'>__Pyx_INCREF</span>(__pyx_t_2);
      <span class='pyx_macro_api'>__Pyx_INCREF</span>(function);
      <span class='pyx_macro_api'>__Pyx_DECREF_SET</span>(__pyx_t_8, function);
    }
  }
  if (!__pyx_t_2) {
    __pyx_t_1 = <span class='pyx_c_api'>__Pyx_PyObject_CallOneArg</span>(__pyx_t_8, __pyx_v_minimosx);<span class='error_goto'> if (unlikely(!__pyx_t_1)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 24; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
    <span class='refnanny'>__Pyx_GOTREF</span>(__pyx_t_1);
  } else {
    __pyx_t_9 = <span class='py_c_api'>PyTuple_New</span>(1+1);<span class='error_goto'> if (unlikely(!__pyx_t_9)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 24; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
    <span class='refnanny'>__Pyx_GOTREF</span>(__pyx_t_9);
    <span class='py_macro_api'>PyTuple_SET_ITEM</span>(__pyx_t_9, 0, __pyx_t_2); <span class='refnanny'>__Pyx_GIVEREF</span>(__pyx_t_2); __pyx_t_2 = NULL;
    <span class='pyx_macro_api'>__Pyx_INCREF</span>(__pyx_v_minimosx);
    <span class='py_macro_api'>PyTuple_SET_ITEM</span>(__pyx_t_9, 0+1, __pyx_v_minimosx);
    <span class='refnanny'>__Pyx_GIVEREF</span>(__pyx_v_minimosx);
    __pyx_t_1 = <span class='pyx_c_api'>__Pyx_PyObject_Call</span>(__pyx_t_8, __pyx_t_9, NULL);<span class='error_goto'> if (unlikely(!__pyx_t_1)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 24; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
    <span class='refnanny'>__Pyx_GOTREF</span>(__pyx_t_1);
    <span class='pyx_macro_api'>__Pyx_DECREF</span>(__pyx_t_9); __pyx_t_9 = 0;
  }
  <span class='pyx_macro_api'>__Pyx_DECREF</span>(__pyx_t_8); __pyx_t_8 = 0;
  __pyx_t_9 = <span class='pyx_c_api'>__Pyx_GetModuleGlobalName</span>(__pyx_n_s_np);<span class='error_goto'> if (unlikely(!__pyx_t_9)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 24; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
  <span class='refnanny'>__Pyx_GOTREF</span>(__pyx_t_9);
  __pyx_t_2 = <span class='pyx_c_api'>__Pyx_PyObject_GetAttrStr</span>(__pyx_t_9, __pyx_n_s_array);<span class='error_goto'> if (unlikely(!__pyx_t_2)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 24; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
  <span class='refnanny'>__Pyx_GOTREF</span>(__pyx_t_2);
  <span class='pyx_macro_api'>__Pyx_DECREF</span>(__pyx_t_9); __pyx_t_9 = 0;
  __pyx_t_9 = NULL;
  if (CYTHON_COMPILING_IN_CPYTHON && unlikely(<span class='py_c_api'>PyMethod_Check</span>(__pyx_t_2))) {
    __pyx_t_9 = <span class='py_macro_api'>PyMethod_GET_SELF</span>(__pyx_t_2);
    if (likely(__pyx_t_9)) {
      PyObject* function = <span class='py_macro_api'>PyMethod_GET_FUNCTION</span>(__pyx_t_2);
      <span class='pyx_macro_api'>__Pyx_INCREF</span>(__pyx_t_9);
      <span class='pyx_macro_api'>__Pyx_INCREF</span>(function);
      <span class='pyx_macro_api'>__Pyx_DECREF_SET</span>(__pyx_t_2, function);
    }
  }
  if (!__pyx_t_9) {
    __pyx_t_8 = <span class='pyx_c_api'>__Pyx_PyObject_CallOneArg</span>(__pyx_t_2, __pyx_v_minimosy);<span class='error_goto'> if (unlikely(!__pyx_t_8)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 24; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
    <span class='refnanny'>__Pyx_GOTREF</span>(__pyx_t_8);
  } else {
    __pyx_t_12 = <span class='py_c_api'>PyTuple_New</span>(1+1);<span class='error_goto'> if (unlikely(!__pyx_t_12)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 24; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
    <span class='refnanny'>__Pyx_GOTREF</span>(__pyx_t_12);
    <span class='py_macro_api'>PyTuple_SET_ITEM</span>(__pyx_t_12, 0, __pyx_t_9); <span class='refnanny'>__Pyx_GIVEREF</span>(__pyx_t_9); __pyx_t_9 = NULL;
    <span class='pyx_macro_api'>__Pyx_INCREF</span>(__pyx_v_minimosy);
    <span class='py_macro_api'>PyTuple_SET_ITEM</span>(__pyx_t_12, 0+1, __pyx_v_minimosy);
    <span class='refnanny'>__Pyx_GIVEREF</span>(__pyx_v_minimosy);
    __pyx_t_8 = <span class='pyx_c_api'>__Pyx_PyObject_Call</span>(__pyx_t_2, __pyx_t_12, NULL);<span class='error_goto'> if (unlikely(!__pyx_t_8)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 24; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
    <span class='refnanny'>__Pyx_GOTREF</span>(__pyx_t_8);
    <span class='pyx_macro_api'>__Pyx_DECREF</span>(__pyx_t_12); __pyx_t_12 = 0;
  }
  <span class='pyx_macro_api'>__Pyx_DECREF</span>(__pyx_t_2); __pyx_t_2 = 0;
  __pyx_t_2 = <span class='py_c_api'>PyTuple_New</span>(2);<span class='error_goto'> if (unlikely(!__pyx_t_2)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 24; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
  <span class='refnanny'>__Pyx_GOTREF</span>(__pyx_t_2);
  <span class='py_macro_api'>PyTuple_SET_ITEM</span>(__pyx_t_2, 0, __pyx_t_1);
  <span class='refnanny'>__Pyx_GIVEREF</span>(__pyx_t_1);
  <span class='py_macro_api'>PyTuple_SET_ITEM</span>(__pyx_t_2, 1, __pyx_t_8);
  <span class='refnanny'>__Pyx_GIVEREF</span>(__pyx_t_8);
  __pyx_t_1 = 0;
  __pyx_t_8 = 0;
  __pyx_r = ((PyObject*)__pyx_t_2);
  __pyx_t_2 = 0;
  goto __pyx_L0;
</pre>
            
            <pre class='cython line score-0'>&#xA0;25: </pre>
            
            <pre class='cython line score-14' onclick='toggleDiv(this)'>+26: <span class="k">def</span> <span class="nf">busca_min_cython3</span><span class="p">(</span><span class="n">malla</span><span class="p">):</span></pre>
            
            <pre class='cython code score-14'>/* Python wrapper */
static PyObject *__pyx_pw_46_cython_magic_b76d9f95ffc9db5b7e97e92e04623490_1busca_min_cython3(PyObject *__pyx_self, PyObject *__pyx_v_malla); /*proto*/
static PyMethodDef __pyx_mdef_46_cython_magic_b76d9f95ffc9db5b7e97e92e04623490_1busca_min_cython3 = {"busca_min_cython3", (PyCFunction)__pyx_pw_46_cython_magic_b76d9f95ffc9db5b7e97e92e04623490_1busca_min_cython3, METH_O, 0};
static PyObject *__pyx_pw_46_cython_magic_b76d9f95ffc9db5b7e97e92e04623490_1busca_min_cython3(PyObject *__pyx_self, PyObject *__pyx_v_malla) {
  PyObject *__pyx_r = 0;
  <span class='refnanny'>__Pyx_RefNannyDeclarations</span>
  <span class='refnanny'>__Pyx_RefNannySetupContext</span>("busca_min_cython3 (wrapper)", 0);
  __pyx_r = __pyx_pf_46_cython_magic_b76d9f95ffc9db5b7e97e92e04623490_busca_min_cython3(__pyx_self, ((PyObject *)__pyx_v_malla));

  /* function exit code */
  <span class='refnanny'>__Pyx_RefNannyFinishContext</span>();
  return __pyx_r;
}

static PyObject *__pyx_pf_46_cython_magic_b76d9f95ffc9db5b7e97e92e04623490_busca_min_cython3(CYTHON_UNUSED PyObject *__pyx_self, PyObject *__pyx_v_malla) {
  PyObject *__pyx_r = NULL;
  <span class='refnanny'>__Pyx_RefNannyDeclarations</span>
  <span class='refnanny'>__Pyx_RefNannySetupContext</span>("busca_min_cython3", 0);
/* … */
  /* function exit code */
  __pyx_L1_error:;
  <span class='pyx_macro_api'>__Pyx_XDECREF</span>(__pyx_t_1);
  <span class='pyx_c_api'>__Pyx_AddTraceback</span>("_cython_magic_b76d9f95ffc9db5b7e97e92e04623490.busca_min_cython3", __pyx_clineno, __pyx_lineno, __pyx_filename);
  __pyx_r = NULL;
  __pyx_L0:;
  <span class='refnanny'>__Pyx_XGIVEREF</span>(__pyx_r);
  <span class='refnanny'>__Pyx_RefNannyFinishContext</span>();
  return __pyx_r;
}
/* … */
  __pyx_tuple_ = <span class='py_c_api'>PyTuple_Pack</span>(1, __pyx_n_s_malla);<span class='error_goto'> if (unlikely(!__pyx_tuple_)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 26; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
  <span class='refnanny'>__Pyx_GOTREF</span>(__pyx_tuple_);
  <span class='refnanny'>__Pyx_GIVEREF</span>(__pyx_tuple_);
/* … */
  __pyx_t_1 = PyCFunction_NewEx(&__pyx_mdef_46_cython_magic_b76d9f95ffc9db5b7e97e92e04623490_1busca_min_cython3, NULL, __pyx_n_s_cython_magic_b76d9f95ffc9db5b7e);<span class='error_goto'> if (unlikely(!__pyx_t_1)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 26; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
  <span class='refnanny'>__Pyx_GOTREF</span>(__pyx_t_1);
  if (<span class='py_c_api'>PyDict_SetItem</span>(__pyx_d, __pyx_n_s_busca_min_cython3, __pyx_t_1) &lt; 0) <span class='error_goto'>{__pyx_filename = __pyx_f[0]; __pyx_lineno = 26; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
  <span class='pyx_macro_api'>__Pyx_DECREF</span>(__pyx_t_1); __pyx_t_1 = 0;
</pre>
            
            <pre class='cython line score-1' onclick='toggleDiv(this)'>+27:     <span class="k">return</span> <span class="n">cbusca_min_cython3</span><span class="p">(</span><span class="n">malla</span><span class="p">)</span></pre>
            
            <pre class='cython code score-1'>  <span class='pyx_macro_api'>__Pyx_XDECREF</span>(__pyx_r);
  __pyx_t_1 = __pyx_f_46_cython_magic_b76d9f95ffc9db5b7e97e92e04623490_cbusca_min_cython3(__pyx_v_malla);<span class='error_goto'> if (unlikely(!__pyx_t_1)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 27; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
  <span class='refnanny'>__Pyx_GOTREF</span>(__pyx_t_1);
  __pyx_r = __pyx_t_1;
  __pyx_t_1 = 0;
  goto __pyx_L0;
</pre>
          </div>
          
          <p>
            </body></html> </div> </div> </div> </div> </div> 
            
            <div>
              <div>
              </div>
              
              <div>
                <div>
                  El <code>if</code> parece la parte más lenta. Estamos usando el valor de entrada que no tiene un tipo Cython definido.<br /> Los bucles parece que están optimizados (las variables envueltas en el bucle las hemos declarado como <code>unsigned int</code>).<br /> Pero todas las partes por las que pasa el numpy array parece que no están muy optimizadas...</p>
                </div>
              </div>
            </div>
            
            <div>
              <div>
              </div>
              
              <div>
                <div>
                  <h1 id="Cythonizando,-que-es-gerundio-(toma-4).">
                    Cythonizando, que es gerundio (toma 4).<a class="anchor-link" href="#Cythonizando,-que-es-gerundio-(toma-4).">&#182;</a>
                  </h1>
                </div>
              </div>
            </div>
            
            <div>
              <div>
              </div>
              
              <div>
                <div>
                  Ahora mismo, haciendo <code>import numpy as np</code> tenemos acceso a la funcionalidad Python de numpy. Para poder acceder a la funcionalidad C de numpy hemos de hacer un <code>cimport</code> de numpy.<br /> El <code>cimport</code> se usa para importar información especial del módulo numpy en el momento de compilación. Esta información se encuentra en el fichero numpy.pxd que es parte de la distribución Cython. El <code>cimport</code> también se usa para poder importar desde la <em>stdlib</em> de C.<br /> Vamos a usar esto para declarar el tipo del array de numpy.</p>
                </div>
              </div>
            </div>
            
            <div>
              <div>
                <div>
                  <div>
                    <div class=" highlight hl-ipython3">
                      <pre><span class="o">%%</span><span class="n">cython</span> <span class="o">--</span><span class="n">name</span> <span class="n">probandocython4</span>
<span class="k">import</span> <span class="nn">numpy</span> <span class="k">as</span> <span class="nn">np</span>
<span class="k">cimport</span> <span class="nn">numpy</span> <span class="k">as</span> <span class="nn">np</span>

<span class="k">cpdef</span> <span class="kt">tuple</span> <span class="nf">busca_min_cython4</span><span class="p">(</span><span class="n">np</span><span class="o">.</span><span class="n">ndarray</span><span class="p">[</span><span class="n">double</span><span class="p">,</span> <span class="n">ndim</span> <span class="o">=</span> <span class="mf">2</span><span class="p">]</span> <span class="n">malla</span><span class="p">):</span>
    <span class="k">cdef</span> <span class="kt">list</span> <span class="nf">minimosx</span><span class="p">,</span> <span class="nf">minimosy</span>
    <span class="k">cdef</span> <span class="kt">unsigned</span> <span class="kt">int</span> <span class="nf">i</span><span class="p">,</span> <span class="nf">j</span>
    <span class="k">cdef</span> <span class="kt">unsigned</span> <span class="kt">int</span> <span class="nf">ii</span> <span class="o">=</span> <span class="n">malla</span><span class="o">.</span><span class="n">shape</span><span class="p">[</span><span class="mf">1</span><span class="p">]</span><span class="o">-</span><span class="mf">1</span>
    <span class="k">cdef</span> <span class="kt">unsigned</span> <span class="kt">int</span> <span class="nf">jj</span> <span class="o">=</span> <span class="n">malla</span><span class="o">.</span><span class="n">shape</span><span class="p">[</span><span class="mf"></span><span class="p">]</span><span class="o">-</span><span class="mf">1</span>
    <span class="k">cdef</span> <span class="kt">unsigned</span> <span class="kt">int</span> <span class="nf">start</span> <span class="o">=</span> <span class="mf">1</span>
    <span class="n">minimosx</span> <span class="o">=</span> <span class="p">[]</span>
    <span class="n">minimosy</span> <span class="o">=</span> <span class="p">[]</span>
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
                      <pre><span class="o">%</span><span class="k">timeit</span> busca_min_cython4(data)
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
                      <pre>10 loops, best of 3: 147 ms per loop
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
                  Guauuuu!!! Acabamos de obtener un incremento de entre 25x a 30x veces más rápido.</p>
                </div>
              </div>
            </div>
            
            <div>
              <div>
              </div>
              
              <div>
                <div>
                  Vamos a comprobar que el resultado sea el mismo que la función original:</p>
                </div>
              </div>
            </div>
            
            <div>
              <div>
                <div>
                  <div>
                    <div class=" highlight hl-ipython3">
                      <pre><span class="n">a</span><span class="p">,</span> <span class="n">b</span> <span class="o">=</span> <span class="n">busca_min</span><span class="p">(</span><span class="n">data</span><span class="p">)</span>
<span class="nb">print</span><span class="p">(</span><span class="n">a</span><span class="p">)</span>
<span class="nb">print</span><span class="p">(</span><span class="n">b</span><span class="p">)</span>
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
                      <pre>[   1    1    1 ..., 1998 1998 1998]
[   1    3   11 ..., 1968 1977 1985]
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
                      <pre><span class="n">aa</span><span class="p">,</span> <span class="n">bb</span> <span class="o">=</span> <span class="n">busca_min_cython4</span><span class="p">(</span><span class="n">data</span><span class="p">)</span>
<span class="nb">print</span><span class="p">(</span><span class="n">aa</span><span class="p">)</span>
<span class="nb">print</span><span class="p">(</span><span class="n">bb</span><span class="p">)</span>
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
                      <pre>[   1    1    1 ..., 1998 1998 1998]
[   1    3   11 ..., 1968 1977 1985]
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
                      <pre><span class="nb">print</span><span class="p">(</span><span class="n">np</span><span class="o">.</span><span class="n">array_equal</span><span class="p">(</span><span class="n">a</span><span class="p">,</span> <span class="n">aa</span><span class="p">))</span>
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
                      <pre>True
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
                      <pre><span class="nb">print</span><span class="p">(</span><span class="n">np</span><span class="o">.</span><span class="n">array_equal</span><span class="p">(</span><span class="n">b</span><span class="p">,</span> <span class="n">bb</span><span class="p">))</span>
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
                      <pre>True
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
                  Pues parece que sí 🙂</p>
                </div>
              </div>
            </div>
            
            <div>
              <div>
              </div>
              
              <div>
                <div>
                  Vamos a ver si hemos dejado la mayoría del código anterior en blanco o más clarito usando <code>--annotate</code>.</p>
                </div>
              </div>
            </div>
            
            <div>
              <div>
                <div>
                  <div>
                    <div class=" highlight hl-ipython3">
                      <pre><span class="o">%%</span><span class="n">cython</span> <span class="o">--</span><span class="n">annotate</span>
<span class="k">import</span> <span class="nn">numpy</span> <span class="k">as</span> <span class="nn">np</span>
<span class="k">cimport</span> <span class="nn">numpy</span> <span class="k">as</span> <span class="nn">np</span>

<span class="k">cpdef</span> <span class="kt">tuple</span> <span class="nf">busca_min_cython4</span><span class="p">(</span><span class="n">np</span><span class="o">.</span><span class="n">ndarray</span><span class="p">[</span><span class="n">double</span><span class="p">,</span> <span class="n">ndim</span> <span class="o">=</span> <span class="mf">2</span><span class="p">]</span> <span class="n">malla</span><span class="p">):</span>
    <span class="k">cdef</span> <span class="kt">list</span> <span class="nf">minimosx</span><span class="p">,</span> <span class="nf">minimosy</span>
    <span class="k">cdef</span> <span class="kt">unsigned</span> <span class="kt">int</span> <span class="nf">i</span><span class="p">,</span> <span class="nf">j</span>
    <span class="k">cdef</span> <span class="kt">unsigned</span> <span class="kt">int</span> <span class="nf">ii</span> <span class="o">=</span> <span class="n">malla</span><span class="o">.</span><span class="n">shape</span><span class="p">[</span><span class="mf">1</span><span class="p">]</span><span class="o">-</span><span class="mf">1</span>
    <span class="k">cdef</span> <span class="kt">unsigned</span> <span class="kt">int</span> <span class="nf">jj</span> <span class="o">=</span> <span class="n">malla</span><span class="o">.</span><span class="n">shape</span><span class="p">[</span><span class="mf"></span><span class="p">]</span><span class="o">-</span><span class="mf">1</span>
    <span class="k">cdef</span> <span class="kt">unsigned</span> <span class="kt">int</span> <span class="nf">start</span> <span class="o">=</span> <span class="mf">1</span>
    <span class="n">minimosx</span> <span class="o">=</span> <span class="p">[]</span>
    <span class="n">minimosy</span> <span class="o">=</span> <span class="p">[]</span>
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
              
              <div>
                <div>
                  <div>
                    <div>
                    </div>
                    
                    <div>
                      <br /> <!-- Generated by Cython 0.22 -->
                      
                      <br /> <br /> <br /> <br /> Generated by Cython 0.22</p> 
                      
                      <div class="cython">
                        <pre class='cython line score-19' onclick='toggleDiv(this)'>+01: <span class="k">import</span> <span class="nn">numpy</span> <span class="k">as</span> <span class="nn">np</span></pre>
                        
                        <pre class='cython code score-19'>  __pyx_t_1 = <span class='pyx_c_api'>__Pyx_Import</span>(__pyx_n_s_numpy, 0, -1);<span class='error_goto'> if (unlikely(!__pyx_t_1)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 1; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
  <span class='refnanny'>__Pyx_GOTREF</span>(__pyx_t_1);
  if (<span class='py_c_api'>PyDict_SetItem</span>(__pyx_d, __pyx_n_s_np, __pyx_t_1) &lt; 0) <span class='error_goto'>{__pyx_filename = __pyx_f[0]; __pyx_lineno = 1; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
  <span class='pyx_macro_api'>__Pyx_DECREF</span>(__pyx_t_1); __pyx_t_1 = 0;
/* … */
  __pyx_t_1 = <span class='py_c_api'>PyDict_New</span>();<span class='error_goto'> if (unlikely(!__pyx_t_1)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 1; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
  <span class='refnanny'>__Pyx_GOTREF</span>(__pyx_t_1);
  if (<span class='py_c_api'>PyDict_SetItem</span>(__pyx_d, __pyx_n_s_test, __pyx_t_1) &lt; 0) <span class='error_goto'>{__pyx_filename = __pyx_f[0]; __pyx_lineno = 1; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
  <span class='pyx_macro_api'>__Pyx_DECREF</span>(__pyx_t_1); __pyx_t_1 = 0;
</pre>
                        
                        <pre class='cython line score-0'>&#xA0;02: <span class="k">cimport</span> <span class="nn">numpy</span> <span class="k">as</span> <span class="nn">np</span></pre>
                        
                        <pre class='cython line score-0'>&#xA0;03: </pre>
                        
                        <pre class='cython line score-35' onclick='toggleDiv(this)'>+04: <span class="k">cpdef</span> <span class="kt">tuple</span> <span class="nf">busca_min_cython4</span><span class="p">(</span><span class="n">np</span><span class="o">.</span><span class="n">ndarray</span><span class="p">[</span><span class="n">double</span><span class="p">,</span> <span class="n">ndim</span> <span class="o">=</span> <span class="mf">2</span><span class="p">]</span> <span class="n">malla</span><span class="p">):</span></pre>
                        
                        <pre class='cython code score-35'>static PyObject *__pyx_pw_46_cython_magic_db10c794e43f00f7b90f23a8e05093c1_1busca_min_cython4(PyObject *__pyx_self, PyObject *__pyx_v_malla); /*proto*/
static PyObject *__pyx_f_46_cython_magic_db10c794e43f00f7b90f23a8e05093c1_busca_min_cython4(PyArrayObject *__pyx_v_malla, CYTHON_UNUSED int __pyx_skip_dispatch) {
  PyObject *__pyx_v_minimosx = 0;
  PyObject *__pyx_v_minimosy = 0;
  unsigned int __pyx_v_i;
  unsigned int __pyx_v_j;
  unsigned int __pyx_v_ii;
  unsigned int __pyx_v_jj;
  unsigned int __pyx_v_start;
  __Pyx_LocalBuf_ND __pyx_pybuffernd_malla;
  __Pyx_Buffer __pyx_pybuffer_malla;
  PyObject *__pyx_r = NULL;
  <span class='refnanny'>__Pyx_RefNannyDeclarations</span>
  <span class='refnanny'>__Pyx_RefNannySetupContext</span>("busca_min_cython4", 0);
  __pyx_pybuffer_malla.pybuffer.buf = NULL;
  __pyx_pybuffer_malla.refcount = 0;
  __pyx_pybuffernd_malla.data = NULL;
  __pyx_pybuffernd_malla.rcbuffer = &__pyx_pybuffer_malla;
  {
    __Pyx_BufFmt_StackElem __pyx_stack[1];
    if (unlikely(<span class='pyx_c_api'>__Pyx_GetBufferAndValidate</span>(&__pyx_pybuffernd_malla.rcbuffer-&gt;pybuffer, (PyObject*)__pyx_v_malla, &__Pyx_TypeInfo_double, PyBUF_FORMAT| PyBUF_STRIDES, 2, 0, __pyx_stack) == -1)) <span class='error_goto'>{__pyx_filename = __pyx_f[0]; __pyx_lineno = 4; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
  }
  __pyx_pybuffernd_malla.diminfo[0].strides = __pyx_pybuffernd_malla.rcbuffer-&gt;pybuffer.strides[0]; __pyx_pybuffernd_malla.diminfo[0].shape = __pyx_pybuffernd_malla.rcbuffer-&gt;pybuffer.shape[0]; __pyx_pybuffernd_malla.diminfo[1].strides = __pyx_pybuffernd_malla.rcbuffer-&gt;pybuffer.strides[1]; __pyx_pybuffernd_malla.diminfo[1].shape = __pyx_pybuffernd_malla.rcbuffer-&gt;pybuffer.shape[1];
/* … */
  /* function exit code */
  __pyx_L1_error:;
  <span class='pyx_macro_api'>__Pyx_XDECREF</span>(__pyx_t_1);
  <span class='pyx_macro_api'>__Pyx_XDECREF</span>(__pyx_t_42);
  <span class='pyx_macro_api'>__Pyx_XDECREF</span>(__pyx_t_43);
  <span class='pyx_macro_api'>__Pyx_XDECREF</span>(__pyx_t_44);
  <span class='pyx_macro_api'>__Pyx_XDECREF</span>(__pyx_t_45);
  { PyObject *__pyx_type, *__pyx_value, *__pyx_tb;
    <span class='pyx_c_api'>__Pyx_ErrFetch</span>(&__pyx_type, &__pyx_value, &__pyx_tb);
    <span class='pyx_c_api'>__Pyx_SafeReleaseBuffer</span>(&__pyx_pybuffernd_malla.rcbuffer-&gt;pybuffer);
  <span class='pyx_c_api'>__Pyx_ErrRestore</span>(__pyx_type, __pyx_value, __pyx_tb);}
  <span class='pyx_c_api'>__Pyx_AddTraceback</span>("_cython_magic_db10c794e43f00f7b90f23a8e05093c1.busca_min_cython4", __pyx_clineno, __pyx_lineno, __pyx_filename);
  __pyx_r = 0;
  goto __pyx_L2;
  __pyx_L0:;
  <span class='pyx_c_api'>__Pyx_SafeReleaseBuffer</span>(&__pyx_pybuffernd_malla.rcbuffer-&gt;pybuffer);
  __pyx_L2:;
  <span class='pyx_macro_api'>__Pyx_XDECREF</span>(__pyx_v_minimosx);
  <span class='pyx_macro_api'>__Pyx_XDECREF</span>(__pyx_v_minimosy);
  <span class='refnanny'>__Pyx_XGIVEREF</span>(__pyx_r);
  <span class='refnanny'>__Pyx_RefNannyFinishContext</span>();
  return __pyx_r;
}

/* Python wrapper */
static PyObject *__pyx_pw_46_cython_magic_db10c794e43f00f7b90f23a8e05093c1_1busca_min_cython4(PyObject *__pyx_self, PyObject *__pyx_v_malla); /*proto*/
static PyObject *__pyx_pw_46_cython_magic_db10c794e43f00f7b90f23a8e05093c1_1busca_min_cython4(PyObject *__pyx_self, PyObject *__pyx_v_malla) {
  PyObject *__pyx_r = 0;
  <span class='refnanny'>__Pyx_RefNannyDeclarations</span>
  <span class='refnanny'>__Pyx_RefNannySetupContext</span>("busca_min_cython4 (wrapper)", 0);
  if (unlikely(!<span class='pyx_c_api'>__Pyx_ArgTypeTest</span>(((PyObject *)__pyx_v_malla), __pyx_ptype_5numpy_ndarray, 1, "malla", 0))) <span class='error_goto'>{__pyx_filename = __pyx_f[0]; __pyx_lineno = 4; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
  __pyx_r = __pyx_pf_46_cython_magic_db10c794e43f00f7b90f23a8e05093c1_busca_min_cython4(__pyx_self, ((PyArrayObject *)__pyx_v_malla));
  CYTHON_UNUSED int __pyx_lineno = 0;
  CYTHON_UNUSED const char *__pyx_filename = NULL;
  CYTHON_UNUSED int __pyx_clineno = 0;

  /* function exit code */
  goto __pyx_L0;
  __pyx_L1_error:;
  __pyx_r = NULL;
  __pyx_L0:;
  <span class='refnanny'>__Pyx_RefNannyFinishContext</span>();
  return __pyx_r;
}

static PyObject *__pyx_pf_46_cython_magic_db10c794e43f00f7b90f23a8e05093c1_busca_min_cython4(CYTHON_UNUSED PyObject *__pyx_self, PyArrayObject *__pyx_v_malla) {
  __Pyx_LocalBuf_ND __pyx_pybuffernd_malla;
  __Pyx_Buffer __pyx_pybuffer_malla;
  PyObject *__pyx_r = NULL;
  <span class='refnanny'>__Pyx_RefNannyDeclarations</span>
  <span class='refnanny'>__Pyx_RefNannySetupContext</span>("busca_min_cython4", 0);
  __pyx_pybuffer_malla.pybuffer.buf = NULL;
  __pyx_pybuffer_malla.refcount = 0;
  __pyx_pybuffernd_malla.data = NULL;
  __pyx_pybuffernd_malla.rcbuffer = &__pyx_pybuffer_malla;
  {
    __Pyx_BufFmt_StackElem __pyx_stack[1];
    if (unlikely(<span class='pyx_c_api'>__Pyx_GetBufferAndValidate</span>(&__pyx_pybuffernd_malla.rcbuffer-&gt;pybuffer, (PyObject*)__pyx_v_malla, &__Pyx_TypeInfo_double, PyBUF_FORMAT| PyBUF_STRIDES, 2, 0, __pyx_stack) == -1)) <span class='error_goto'>{__pyx_filename = __pyx_f[0]; __pyx_lineno = 4; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
  }
  __pyx_pybuffernd_malla.diminfo[0].strides = __pyx_pybuffernd_malla.rcbuffer-&gt;pybuffer.strides[0]; __pyx_pybuffernd_malla.diminfo[0].shape = __pyx_pybuffernd_malla.rcbuffer-&gt;pybuffer.shape[0]; __pyx_pybuffernd_malla.diminfo[1].strides = __pyx_pybuffernd_malla.rcbuffer-&gt;pybuffer.strides[1]; __pyx_pybuffernd_malla.diminfo[1].shape = __pyx_pybuffernd_malla.rcbuffer-&gt;pybuffer.shape[1];
  <span class='pyx_macro_api'>__Pyx_XDECREF</span>(__pyx_r);
  __pyx_t_1 = __pyx_f_46_cython_magic_db10c794e43f00f7b90f23a8e05093c1_busca_min_cython4(__pyx_v_malla, 0);<span class='error_goto'> if (unlikely(!__pyx_t_1)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 4; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
  <span class='refnanny'>__Pyx_GOTREF</span>(__pyx_t_1);
  __pyx_r = __pyx_t_1;
  __pyx_t_1 = 0;
  goto __pyx_L0;

  /* function exit code */
  __pyx_L1_error:;
  <span class='pyx_macro_api'>__Pyx_XDECREF</span>(__pyx_t_1);
  { PyObject *__pyx_type, *__pyx_value, *__pyx_tb;
    <span class='pyx_c_api'>__Pyx_ErrFetch</span>(&__pyx_type, &__pyx_value, &__pyx_tb);
    <span class='pyx_c_api'>__Pyx_SafeReleaseBuffer</span>(&__pyx_pybuffernd_malla.rcbuffer-&gt;pybuffer);
  <span class='pyx_c_api'>__Pyx_ErrRestore</span>(__pyx_type, __pyx_value, __pyx_tb);}
  <span class='pyx_c_api'>__Pyx_AddTraceback</span>("_cython_magic_db10c794e43f00f7b90f23a8e05093c1.busca_min_cython4", __pyx_clineno, __pyx_lineno, __pyx_filename);
  __pyx_r = NULL;
  goto __pyx_L2;
  __pyx_L0:;
  <span class='pyx_c_api'>__Pyx_SafeReleaseBuffer</span>(&__pyx_pybuffernd_malla.rcbuffer-&gt;pybuffer);
  __pyx_L2:;
  <span class='refnanny'>__Pyx_XGIVEREF</span>(__pyx_r);
  <span class='refnanny'>__Pyx_RefNannyFinishContext</span>();
  return __pyx_r;
}
</pre>
                        
                        <pre class='cython line score-0'>&#xA0;05:     <span class="k">cdef</span> <span class="kt">list</span> <span class="nf">minimosx</span><span class="p">,</span> <span class="nf">minimosy</span></pre>
                        
                        <pre class='cython line score-0'>&#xA0;06:     <span class="k">cdef</span> <span class="kt">unsigned</span> <span class="kt">int</span> <span class="nf">i</span><span class="p">,</span> <span class="nf">j</span></pre>
                        
                        <pre class='cython line score-0' onclick='toggleDiv(this)'>+07:     <span class="k">cdef</span> <span class="kt">unsigned</span> <span class="kt">int</span> <span class="nf">ii</span> <span class="o">=</span> <span class="n">malla</span><span class="o">.</span><span class="n">shape</span><span class="p">[</span><span class="mf">1</span><span class="p">]</span><span class="o">-</span><span class="mf">1</span></pre>
                        
                        <pre class='cython code score-0'>  __pyx_v_ii = ((__pyx_v_malla-&gt;dimensions[1]) - 1);
</pre>
                        
                        <pre class='cython line score-0' onclick='toggleDiv(this)'>+08:     <span class="k">cdef</span> <span class="kt">unsigned</span> <span class="kt">int</span> <span class="nf">jj</span> <span class="o">=</span> <span class="n">malla</span><span class="o">.</span><span class="n">shape</span><span class="p">[</span><span class="mf"></span><span class="p">]</span><span class="o">-</span><span class="mf">1</span></pre>
                        
                        <pre class='cython code score-0'>  __pyx_v_jj = ((__pyx_v_malla-&gt;dimensions[0]) - 1);
</pre>
                        
                        <pre class='cython line score-0' onclick='toggleDiv(this)'>+09:     <span class="k">cdef</span> <span class="kt">unsigned</span> <span class="kt">int</span> <span class="nf">start</span> <span class="o">=</span> <span class="mf">1</span></pre>
                        
                        <pre class='cython code score-0'>  __pyx_v_start = 1;
</pre>
                        
                        <pre class='cython line score-5' onclick='toggleDiv(this)'>+10:     <span class="n">minimosx</span> <span class="o">=</span> <span class="p">[]</span></pre>
                        
                        <pre class='cython code score-5'>  __pyx_t_1 = <span class='py_c_api'>PyList_New</span>(0);<span class='error_goto'> if (unlikely(!__pyx_t_1)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 10; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
  <span class='refnanny'>__Pyx_GOTREF</span>(__pyx_t_1);
  __pyx_v_minimosx = ((PyObject*)__pyx_t_1);
  __pyx_t_1 = 0;
</pre>
                        
                        <pre class='cython line score-5' onclick='toggleDiv(this)'>+11:     <span class="n">minimosy</span> <span class="o">=</span> <span class="p">[]</span></pre>
                        
                        <pre class='cython code score-5'>  __pyx_t_1 = <span class='py_c_api'>PyList_New</span>(0);<span class='error_goto'> if (unlikely(!__pyx_t_1)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 11; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
  <span class='refnanny'>__Pyx_GOTREF</span>(__pyx_t_1);
  __pyx_v_minimosy = ((PyObject*)__pyx_t_1);
  __pyx_t_1 = 0;
</pre>
                        
                        <pre class='cython line score-0' onclick='toggleDiv(this)'>+12:     <span class="k">for</span> <span class="n">i</span> <span class="ow">in</span> <span class="nb">range</span><span class="p">(</span><span class="n">start</span><span class="p">,</span> <span class="n">ii</span><span class="p">):</span></pre>
                        
                        <pre class='cython code score-0'>  __pyx_t_2 = __pyx_v_ii;
  for (__pyx_t_3 = __pyx_v_start; __pyx_t_3 &lt; __pyx_t_2; __pyx_t_3+=1) {
    __pyx_v_i = __pyx_t_3;
</pre>
                        
                        <pre class='cython line score-0' onclick='toggleDiv(this)'>+13:         <span class="k">for</span> <span class="n">j</span> <span class="ow">in</span> <span class="nb">range</span><span class="p">(</span><span class="n">start</span><span class="p">,</span> <span class="n">jj</span><span class="p">):</span></pre>
                        
                        <pre class='cython code score-0'>    __pyx_t_4 = __pyx_v_jj;
    for (__pyx_t_5 = __pyx_v_start; __pyx_t_5 &lt; __pyx_t_4; __pyx_t_5+=1) {
      __pyx_v_j = __pyx_t_5;
</pre>
                        
                        <pre class='cython line score-4' onclick='toggleDiv(this)'>+14:             <span class="k">if</span> <span class="p">(</span><span class="n">malla</span><span class="p">[</span><span class="n">j</span><span class="p">,</span> <span class="n">i</span><span class="p">]</span> <span class="o">&lt;</span> <span class="n">malla</span><span class="p">[</span><span class="n">j</span><span class="o">-</span><span class="mf">1</span><span class="p">,</span> <span class="n">i</span><span class="o">-</span><span class="mf">1</span><span class="p">]</span> <span class="ow">and</span></pre>
                        
                        <pre class='cython code score-4'>      __pyx_t_7 = __pyx_v_j;
      __pyx_t_8 = __pyx_v_i;
      __pyx_t_9 = -1;
      if (unlikely(__pyx_t_7 &gt;= (size_t)__pyx_pybuffernd_malla.diminfo[0].shape)) __pyx_t_9 = 0;
      if (unlikely(__pyx_t_8 &gt;= (size_t)__pyx_pybuffernd_malla.diminfo[1].shape)) __pyx_t_9 = 1;
      if (unlikely(__pyx_t_9 != -1)) {
        <span class='pyx_c_api'>__Pyx_RaiseBufferIndexError</span>(__pyx_t_9);
        <span class='error_goto'>{__pyx_filename = __pyx_f[0]; __pyx_lineno = 14; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
      }
      __pyx_t_10 = (__pyx_v_j - 1);
      __pyx_t_11 = (__pyx_v_i - 1);
      __pyx_t_9 = -1;
      if (__pyx_t_10 &lt; 0) {
        __pyx_t_10 += __pyx_pybuffernd_malla.diminfo[0].shape;
        if (unlikely(__pyx_t_10 &lt; 0)) __pyx_t_9 = 0;
      } else if (unlikely(__pyx_t_10 &gt;= __pyx_pybuffernd_malla.diminfo[0].shape)) __pyx_t_9 = 0;
      if (__pyx_t_11 &lt; 0) {
        __pyx_t_11 += __pyx_pybuffernd_malla.diminfo[1].shape;
        if (unlikely(__pyx_t_11 &lt; 0)) __pyx_t_9 = 1;
      } else if (unlikely(__pyx_t_11 &gt;= __pyx_pybuffernd_malla.diminfo[1].shape)) __pyx_t_9 = 1;
      if (unlikely(__pyx_t_9 != -1)) {
        <span class='pyx_c_api'>__Pyx_RaiseBufferIndexError</span>(__pyx_t_9);
        <span class='error_goto'>{__pyx_filename = __pyx_f[0]; __pyx_lineno = 14; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
      }
      __pyx_t_12 = (((*__Pyx_BufPtrStrided2d(double *, __pyx_pybuffernd_malla.rcbuffer-&gt;pybuffer.buf, __pyx_t_7, __pyx_pybuffernd_malla.diminfo[0].strides, __pyx_t_8, __pyx_pybuffernd_malla.diminfo[1].strides)) &lt; (*__Pyx_BufPtrStrided2d(double *, __pyx_pybuffernd_malla.rcbuffer-&gt;pybuffer.buf, __pyx_t_10, __pyx_pybuffernd_malla.diminfo[0].strides, __pyx_t_11, __pyx_pybuffernd_malla.diminfo[1].strides))) != 0);
      if (__pyx_t_12) {
      } else {
        __pyx_t_6 = __pyx_t_12;
        goto __pyx_L8_bool_binop_done;
      }
</pre>
                        
                        <pre class='cython line score-4' onclick='toggleDiv(this)'>+15:                 <span class="n">malla</span><span class="p">[</span><span class="n">j</span><span class="p">,</span> <span class="n">i</span><span class="p">]</span> <span class="o">&lt;</span> <span class="n">malla</span><span class="p">[</span><span class="n">j</span><span class="o">-</span><span class="mf">1</span><span class="p">,</span> <span class="n">i</span><span class="p">]</span> <span class="ow">and</span></pre>
                        
                        <pre class='cython code score-4'>      __pyx_t_13 = __pyx_v_j;
      __pyx_t_14 = __pyx_v_i;
      __pyx_t_9 = -1;
      if (unlikely(__pyx_t_13 &gt;= (size_t)__pyx_pybuffernd_malla.diminfo[0].shape)) __pyx_t_9 = 0;
      if (unlikely(__pyx_t_14 &gt;= (size_t)__pyx_pybuffernd_malla.diminfo[1].shape)) __pyx_t_9 = 1;
      if (unlikely(__pyx_t_9 != -1)) {
        <span class='pyx_c_api'>__Pyx_RaiseBufferIndexError</span>(__pyx_t_9);
        <span class='error_goto'>{__pyx_filename = __pyx_f[0]; __pyx_lineno = 15; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
      }
      __pyx_t_15 = (__pyx_v_j - 1);
      __pyx_t_16 = __pyx_v_i;
      __pyx_t_9 = -1;
      if (__pyx_t_15 &lt; 0) {
        __pyx_t_15 += __pyx_pybuffernd_malla.diminfo[0].shape;
        if (unlikely(__pyx_t_15 &lt; 0)) __pyx_t_9 = 0;
      } else if (unlikely(__pyx_t_15 &gt;= __pyx_pybuffernd_malla.diminfo[0].shape)) __pyx_t_9 = 0;
      if (unlikely(__pyx_t_16 &gt;= (size_t)__pyx_pybuffernd_malla.diminfo[1].shape)) __pyx_t_9 = 1;
      if (unlikely(__pyx_t_9 != -1)) {
        <span class='pyx_c_api'>__Pyx_RaiseBufferIndexError</span>(__pyx_t_9);
        <span class='error_goto'>{__pyx_filename = __pyx_f[0]; __pyx_lineno = 15; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
      }
      __pyx_t_12 = (((*__Pyx_BufPtrStrided2d(double *, __pyx_pybuffernd_malla.rcbuffer-&gt;pybuffer.buf, __pyx_t_13, __pyx_pybuffernd_malla.diminfo[0].strides, __pyx_t_14, __pyx_pybuffernd_malla.diminfo[1].strides)) &lt; (*__Pyx_BufPtrStrided2d(double *, __pyx_pybuffernd_malla.rcbuffer-&gt;pybuffer.buf, __pyx_t_15, __pyx_pybuffernd_malla.diminfo[0].strides, __pyx_t_16, __pyx_pybuffernd_malla.diminfo[1].strides))) != 0);
      if (__pyx_t_12) {
      } else {
        __pyx_t_6 = __pyx_t_12;
        goto __pyx_L8_bool_binop_done;
      }
</pre>
                        
                        <pre class='cython line score-4' onclick='toggleDiv(this)'>+16:                 <span class="n">malla</span><span class="p">[</span><span class="n">j</span><span class="p">,</span> <span class="n">i</span><span class="p">]</span> <span class="o">&lt;</span> <span class="n">malla</span><span class="p">[</span><span class="n">j</span><span class="o">-</span><span class="mf">1</span><span class="p">,</span> <span class="n">i</span><span class="o">+</span><span class="mf">1</span><span class="p">]</span> <span class="ow">and</span></pre>
                        
                        <pre class='cython code score-4'>      __pyx_t_17 = __pyx_v_j;
      __pyx_t_18 = __pyx_v_i;
      __pyx_t_9 = -1;
      if (unlikely(__pyx_t_17 &gt;= (size_t)__pyx_pybuffernd_malla.diminfo[0].shape)) __pyx_t_9 = 0;
      if (unlikely(__pyx_t_18 &gt;= (size_t)__pyx_pybuffernd_malla.diminfo[1].shape)) __pyx_t_9 = 1;
      if (unlikely(__pyx_t_9 != -1)) {
        <span class='pyx_c_api'>__Pyx_RaiseBufferIndexError</span>(__pyx_t_9);
        <span class='error_goto'>{__pyx_filename = __pyx_f[0]; __pyx_lineno = 16; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
      }
      __pyx_t_19 = (__pyx_v_j - 1);
      __pyx_t_20 = (__pyx_v_i + 1);
      __pyx_t_9 = -1;
      if (__pyx_t_19 &lt; 0) {
        __pyx_t_19 += __pyx_pybuffernd_malla.diminfo[0].shape;
        if (unlikely(__pyx_t_19 &lt; 0)) __pyx_t_9 = 0;
      } else if (unlikely(__pyx_t_19 &gt;= __pyx_pybuffernd_malla.diminfo[0].shape)) __pyx_t_9 = 0;
      if (__pyx_t_20 &lt; 0) {
        __pyx_t_20 += __pyx_pybuffernd_malla.diminfo[1].shape;
        if (unlikely(__pyx_t_20 &lt; 0)) __pyx_t_9 = 1;
      } else if (unlikely(__pyx_t_20 &gt;= __pyx_pybuffernd_malla.diminfo[1].shape)) __pyx_t_9 = 1;
      if (unlikely(__pyx_t_9 != -1)) {
        <span class='pyx_c_api'>__Pyx_RaiseBufferIndexError</span>(__pyx_t_9);
        <span class='error_goto'>{__pyx_filename = __pyx_f[0]; __pyx_lineno = 16; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
      }
      __pyx_t_12 = (((*__Pyx_BufPtrStrided2d(double *, __pyx_pybuffernd_malla.rcbuffer-&gt;pybuffer.buf, __pyx_t_17, __pyx_pybuffernd_malla.diminfo[0].strides, __pyx_t_18, __pyx_pybuffernd_malla.diminfo[1].strides)) &lt; (*__Pyx_BufPtrStrided2d(double *, __pyx_pybuffernd_malla.rcbuffer-&gt;pybuffer.buf, __pyx_t_19, __pyx_pybuffernd_malla.diminfo[0].strides, __pyx_t_20, __pyx_pybuffernd_malla.diminfo[1].strides))) != 0);
      if (__pyx_t_12) {
      } else {
        __pyx_t_6 = __pyx_t_12;
        goto __pyx_L8_bool_binop_done;
      }
</pre>
                        
                        <pre class='cython line score-4' onclick='toggleDiv(this)'>+17:                 <span class="n">malla</span><span class="p">[</span><span class="n">j</span><span class="p">,</span> <span class="n">i</span><span class="p">]</span> <span class="o">&lt;</span> <span class="n">malla</span><span class="p">[</span><span class="n">j</span><span class="p">,</span> <span class="n">i</span><span class="o">-</span><span class="mf">1</span><span class="p">]</span> <span class="ow">and</span></pre>
                        
                        <pre class='cython code score-4'>      __pyx_t_21 = __pyx_v_j;
      __pyx_t_22 = __pyx_v_i;
      __pyx_t_9 = -1;
      if (unlikely(__pyx_t_21 &gt;= (size_t)__pyx_pybuffernd_malla.diminfo[0].shape)) __pyx_t_9 = 0;
      if (unlikely(__pyx_t_22 &gt;= (size_t)__pyx_pybuffernd_malla.diminfo[1].shape)) __pyx_t_9 = 1;
      if (unlikely(__pyx_t_9 != -1)) {
        <span class='pyx_c_api'>__Pyx_RaiseBufferIndexError</span>(__pyx_t_9);
        <span class='error_goto'>{__pyx_filename = __pyx_f[0]; __pyx_lineno = 17; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
      }
      __pyx_t_23 = __pyx_v_j;
      __pyx_t_24 = (__pyx_v_i - 1);
      __pyx_t_9 = -1;
      if (unlikely(__pyx_t_23 &gt;= (size_t)__pyx_pybuffernd_malla.diminfo[0].shape)) __pyx_t_9 = 0;
      if (__pyx_t_24 &lt; 0) {
        __pyx_t_24 += __pyx_pybuffernd_malla.diminfo[1].shape;
        if (unlikely(__pyx_t_24 &lt; 0)) __pyx_t_9 = 1;
      } else if (unlikely(__pyx_t_24 &gt;= __pyx_pybuffernd_malla.diminfo[1].shape)) __pyx_t_9 = 1;
      if (unlikely(__pyx_t_9 != -1)) {
        <span class='pyx_c_api'>__Pyx_RaiseBufferIndexError</span>(__pyx_t_9);
        <span class='error_goto'>{__pyx_filename = __pyx_f[0]; __pyx_lineno = 17; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
      }
      __pyx_t_12 = (((*__Pyx_BufPtrStrided2d(double *, __pyx_pybuffernd_malla.rcbuffer-&gt;pybuffer.buf, __pyx_t_21, __pyx_pybuffernd_malla.diminfo[0].strides, __pyx_t_22, __pyx_pybuffernd_malla.diminfo[1].strides)) &lt; (*__Pyx_BufPtrStrided2d(double *, __pyx_pybuffernd_malla.rcbuffer-&gt;pybuffer.buf, __pyx_t_23, __pyx_pybuffernd_malla.diminfo[0].strides, __pyx_t_24, __pyx_pybuffernd_malla.diminfo[1].strides))) != 0);
      if (__pyx_t_12) {
      } else {
        __pyx_t_6 = __pyx_t_12;
        goto __pyx_L8_bool_binop_done;
      }
</pre>
                        
                        <pre class='cython line score-4' onclick='toggleDiv(this)'>+18:                 <span class="n">malla</span><span class="p">[</span><span class="n">j</span><span class="p">,</span> <span class="n">i</span><span class="p">]</span> <span class="o">&lt;</span> <span class="n">malla</span><span class="p">[</span><span class="n">j</span><span class="p">,</span> <span class="n">i</span><span class="o">+</span><span class="mf">1</span><span class="p">]</span> <span class="ow">and</span></pre>
                        
                        <pre class='cython code score-4'>      __pyx_t_25 = __pyx_v_j;
      __pyx_t_26 = __pyx_v_i;
      __pyx_t_9 = -1;
      if (unlikely(__pyx_t_25 &gt;= (size_t)__pyx_pybuffernd_malla.diminfo[0].shape)) __pyx_t_9 = 0;
      if (unlikely(__pyx_t_26 &gt;= (size_t)__pyx_pybuffernd_malla.diminfo[1].shape)) __pyx_t_9 = 1;
      if (unlikely(__pyx_t_9 != -1)) {
        <span class='pyx_c_api'>__Pyx_RaiseBufferIndexError</span>(__pyx_t_9);
        <span class='error_goto'>{__pyx_filename = __pyx_f[0]; __pyx_lineno = 18; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
      }
      __pyx_t_27 = __pyx_v_j;
      __pyx_t_28 = (__pyx_v_i + 1);
      __pyx_t_9 = -1;
      if (unlikely(__pyx_t_27 &gt;= (size_t)__pyx_pybuffernd_malla.diminfo[0].shape)) __pyx_t_9 = 0;
      if (__pyx_t_28 &lt; 0) {
        __pyx_t_28 += __pyx_pybuffernd_malla.diminfo[1].shape;
        if (unlikely(__pyx_t_28 &lt; 0)) __pyx_t_9 = 1;
      } else if (unlikely(__pyx_t_28 &gt;= __pyx_pybuffernd_malla.diminfo[1].shape)) __pyx_t_9 = 1;
      if (unlikely(__pyx_t_9 != -1)) {
        <span class='pyx_c_api'>__Pyx_RaiseBufferIndexError</span>(__pyx_t_9);
        <span class='error_goto'>{__pyx_filename = __pyx_f[0]; __pyx_lineno = 18; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
      }
      __pyx_t_12 = (((*__Pyx_BufPtrStrided2d(double *, __pyx_pybuffernd_malla.rcbuffer-&gt;pybuffer.buf, __pyx_t_25, __pyx_pybuffernd_malla.diminfo[0].strides, __pyx_t_26, __pyx_pybuffernd_malla.diminfo[1].strides)) &lt; (*__Pyx_BufPtrStrided2d(double *, __pyx_pybuffernd_malla.rcbuffer-&gt;pybuffer.buf, __pyx_t_27, __pyx_pybuffernd_malla.diminfo[0].strides, __pyx_t_28, __pyx_pybuffernd_malla.diminfo[1].strides))) != 0);
      if (__pyx_t_12) {
      } else {
        __pyx_t_6 = __pyx_t_12;
        goto __pyx_L8_bool_binop_done;
      }
</pre>
                        
                        <pre class='cython line score-4' onclick='toggleDiv(this)'>+19:                 <span class="n">malla</span><span class="p">[</span><span class="n">j</span><span class="p">,</span> <span class="n">i</span><span class="p">]</span> <span class="o">&lt;</span> <span class="n">malla</span><span class="p">[</span><span class="n">j</span><span class="o">+</span><span class="mf">1</span><span class="p">,</span> <span class="n">i</span><span class="o">-</span><span class="mf">1</span><span class="p">]</span> <span class="ow">and</span></pre>
                        
                        <pre class='cython code score-4'>      __pyx_t_29 = __pyx_v_j;
      __pyx_t_30 = __pyx_v_i;
      __pyx_t_9 = -1;
      if (unlikely(__pyx_t_29 &gt;= (size_t)__pyx_pybuffernd_malla.diminfo[0].shape)) __pyx_t_9 = 0;
      if (unlikely(__pyx_t_30 &gt;= (size_t)__pyx_pybuffernd_malla.diminfo[1].shape)) __pyx_t_9 = 1;
      if (unlikely(__pyx_t_9 != -1)) {
        <span class='pyx_c_api'>__Pyx_RaiseBufferIndexError</span>(__pyx_t_9);
        <span class='error_goto'>{__pyx_filename = __pyx_f[0]; __pyx_lineno = 19; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
      }
      __pyx_t_31 = (__pyx_v_j + 1);
      __pyx_t_32 = (__pyx_v_i - 1);
      __pyx_t_9 = -1;
      if (__pyx_t_31 &lt; 0) {
        __pyx_t_31 += __pyx_pybuffernd_malla.diminfo[0].shape;
        if (unlikely(__pyx_t_31 &lt; 0)) __pyx_t_9 = 0;
      } else if (unlikely(__pyx_t_31 &gt;= __pyx_pybuffernd_malla.diminfo[0].shape)) __pyx_t_9 = 0;
      if (__pyx_t_32 &lt; 0) {
        __pyx_t_32 += __pyx_pybuffernd_malla.diminfo[1].shape;
        if (unlikely(__pyx_t_32 &lt; 0)) __pyx_t_9 = 1;
      } else if (unlikely(__pyx_t_32 &gt;= __pyx_pybuffernd_malla.diminfo[1].shape)) __pyx_t_9 = 1;
      if (unlikely(__pyx_t_9 != -1)) {
        <span class='pyx_c_api'>__Pyx_RaiseBufferIndexError</span>(__pyx_t_9);
        <span class='error_goto'>{__pyx_filename = __pyx_f[0]; __pyx_lineno = 19; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
      }
      __pyx_t_12 = (((*__Pyx_BufPtrStrided2d(double *, __pyx_pybuffernd_malla.rcbuffer-&gt;pybuffer.buf, __pyx_t_29, __pyx_pybuffernd_malla.diminfo[0].strides, __pyx_t_30, __pyx_pybuffernd_malla.diminfo[1].strides)) &lt; (*__Pyx_BufPtrStrided2d(double *, __pyx_pybuffernd_malla.rcbuffer-&gt;pybuffer.buf, __pyx_t_31, __pyx_pybuffernd_malla.diminfo[0].strides, __pyx_t_32, __pyx_pybuffernd_malla.diminfo[1].strides))) != 0);
      if (__pyx_t_12) {
      } else {
        __pyx_t_6 = __pyx_t_12;
        goto __pyx_L8_bool_binop_done;
      }
</pre>
                        
                        <pre class='cython line score-4' onclick='toggleDiv(this)'>+20:                 <span class="n">malla</span><span class="p">[</span><span class="n">j</span><span class="p">,</span> <span class="n">i</span><span class="p">]</span> <span class="o">&lt;</span> <span class="n">malla</span><span class="p">[</span><span class="n">j</span><span class="o">+</span><span class="mf">1</span><span class="p">,</span> <span class="n">i</span><span class="p">]</span> <span class="ow">and</span></pre>
                        
                        <pre class='cython code score-4'>      __pyx_t_33 = __pyx_v_j;
      __pyx_t_34 = __pyx_v_i;
      __pyx_t_9 = -1;
      if (unlikely(__pyx_t_33 &gt;= (size_t)__pyx_pybuffernd_malla.diminfo[0].shape)) __pyx_t_9 = 0;
      if (unlikely(__pyx_t_34 &gt;= (size_t)__pyx_pybuffernd_malla.diminfo[1].shape)) __pyx_t_9 = 1;
      if (unlikely(__pyx_t_9 != -1)) {
        <span class='pyx_c_api'>__Pyx_RaiseBufferIndexError</span>(__pyx_t_9);
        <span class='error_goto'>{__pyx_filename = __pyx_f[0]; __pyx_lineno = 20; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
      }
      __pyx_t_35 = (__pyx_v_j + 1);
      __pyx_t_36 = __pyx_v_i;
      __pyx_t_9 = -1;
      if (__pyx_t_35 &lt; 0) {
        __pyx_t_35 += __pyx_pybuffernd_malla.diminfo[0].shape;
        if (unlikely(__pyx_t_35 &lt; 0)) __pyx_t_9 = 0;
      } else if (unlikely(__pyx_t_35 &gt;= __pyx_pybuffernd_malla.diminfo[0].shape)) __pyx_t_9 = 0;
      if (unlikely(__pyx_t_36 &gt;= (size_t)__pyx_pybuffernd_malla.diminfo[1].shape)) __pyx_t_9 = 1;
      if (unlikely(__pyx_t_9 != -1)) {
        <span class='pyx_c_api'>__Pyx_RaiseBufferIndexError</span>(__pyx_t_9);
        <span class='error_goto'>{__pyx_filename = __pyx_f[0]; __pyx_lineno = 20; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
      }
      __pyx_t_12 = (((*__Pyx_BufPtrStrided2d(double *, __pyx_pybuffernd_malla.rcbuffer-&gt;pybuffer.buf, __pyx_t_33, __pyx_pybuffernd_malla.diminfo[0].strides, __pyx_t_34, __pyx_pybuffernd_malla.diminfo[1].strides)) &lt; (*__Pyx_BufPtrStrided2d(double *, __pyx_pybuffernd_malla.rcbuffer-&gt;pybuffer.buf, __pyx_t_35, __pyx_pybuffernd_malla.diminfo[0].strides, __pyx_t_36, __pyx_pybuffernd_malla.diminfo[1].strides))) != 0);
      if (__pyx_t_12) {
      } else {
        __pyx_t_6 = __pyx_t_12;
        goto __pyx_L8_bool_binop_done;
      }
</pre>
                        
                        <pre class='cython line score-4' onclick='toggleDiv(this)'>+21:                 <span class="n">malla</span><span class="p">[</span><span class="n">j</span><span class="p">,</span> <span class="n">i</span><span class="p">]</span> <span class="o">&lt;</span> <span class="n">malla</span><span class="p">[</span><span class="n">j</span><span class="o">+</span><span class="mf">1</span><span class="p">,</span> <span class="n">i</span><span class="o">+</span><span class="mf">1</span><span class="p">]):</span></pre>
                        
                        <pre class='cython code score-4'>      __pyx_t_37 = __pyx_v_j;
      __pyx_t_38 = __pyx_v_i;
      __pyx_t_9 = -1;
      if (unlikely(__pyx_t_37 &gt;= (size_t)__pyx_pybuffernd_malla.diminfo[0].shape)) __pyx_t_9 = 0;
      if (unlikely(__pyx_t_38 &gt;= (size_t)__pyx_pybuffernd_malla.diminfo[1].shape)) __pyx_t_9 = 1;
      if (unlikely(__pyx_t_9 != -1)) {
        <span class='pyx_c_api'>__Pyx_RaiseBufferIndexError</span>(__pyx_t_9);
        <span class='error_goto'>{__pyx_filename = __pyx_f[0]; __pyx_lineno = 21; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
      }
      __pyx_t_39 = (__pyx_v_j + 1);
      __pyx_t_40 = (__pyx_v_i + 1);
      __pyx_t_9 = -1;
      if (__pyx_t_39 &lt; 0) {
        __pyx_t_39 += __pyx_pybuffernd_malla.diminfo[0].shape;
        if (unlikely(__pyx_t_39 &lt; 0)) __pyx_t_9 = 0;
      } else if (unlikely(__pyx_t_39 &gt;= __pyx_pybuffernd_malla.diminfo[0].shape)) __pyx_t_9 = 0;
      if (__pyx_t_40 &lt; 0) {
        __pyx_t_40 += __pyx_pybuffernd_malla.diminfo[1].shape;
        if (unlikely(__pyx_t_40 &lt; 0)) __pyx_t_9 = 1;
      } else if (unlikely(__pyx_t_40 &gt;= __pyx_pybuffernd_malla.diminfo[1].shape)) __pyx_t_9 = 1;
      if (unlikely(__pyx_t_9 != -1)) {
        <span class='pyx_c_api'>__Pyx_RaiseBufferIndexError</span>(__pyx_t_9);
        <span class='error_goto'>{__pyx_filename = __pyx_f[0]; __pyx_lineno = 21; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
      }
      __pyx_t_12 = (((*__Pyx_BufPtrStrided2d(double *, __pyx_pybuffernd_malla.rcbuffer-&gt;pybuffer.buf, __pyx_t_37, __pyx_pybuffernd_malla.diminfo[0].strides, __pyx_t_38, __pyx_pybuffernd_malla.diminfo[1].strides)) &lt; (*__Pyx_BufPtrStrided2d(double *, __pyx_pybuffernd_malla.rcbuffer-&gt;pybuffer.buf, __pyx_t_39, __pyx_pybuffernd_malla.diminfo[0].strides, __pyx_t_40, __pyx_pybuffernd_malla.diminfo[1].strides))) != 0);
      __pyx_t_6 = __pyx_t_12;
      __pyx_L8_bool_binop_done:;
      if (__pyx_t_6) {
</pre>
                        
                        <pre class='cython line score-5' onclick='toggleDiv(this)'>+22:                 <span class="n">minimosx</span><span class="o">.</span><span class="n">append</span><span class="p">(</span><span class="n">i</span><span class="p">)</span></pre>
                        
                        <pre class='cython code score-5'>        __pyx_t_1 = <span class='pyx_c_api'>__Pyx_PyInt_From_unsigned_int</span>(__pyx_v_i);<span class='error_goto'> if (unlikely(!__pyx_t_1)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 22; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
        <span class='refnanny'>__Pyx_GOTREF</span>(__pyx_t_1);
        __pyx_t_41 = <span class='pyx_c_api'>__Pyx_PyList_Append</span>(__pyx_v_minimosx, __pyx_t_1);<span class='error_goto'> if (unlikely(__pyx_t_41 == -1)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 22; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
        <span class='pyx_macro_api'>__Pyx_DECREF</span>(__pyx_t_1); __pyx_t_1 = 0;
</pre>
                        
                        <pre class='cython line score-5' onclick='toggleDiv(this)'>+23:                 <span class="n">minimosy</span><span class="o">.</span><span class="n">append</span><span class="p">(</span><span class="n">j</span><span class="p">)</span></pre>
                        
                        <pre class='cython code score-5'>        __pyx_t_1 = <span class='pyx_c_api'>__Pyx_PyInt_From_unsigned_int</span>(__pyx_v_j);<span class='error_goto'> if (unlikely(!__pyx_t_1)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 23; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
        <span class='refnanny'>__Pyx_GOTREF</span>(__pyx_t_1);
        __pyx_t_41 = <span class='pyx_c_api'>__Pyx_PyList_Append</span>(__pyx_v_minimosy, __pyx_t_1);<span class='error_goto'> if (unlikely(__pyx_t_41 == -1)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 23; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
        <span class='pyx_macro_api'>__Pyx_DECREF</span>(__pyx_t_1); __pyx_t_1 = 0;
        goto __pyx_L7;
      }
      __pyx_L7:;
    }
  }
</pre>
                        
                        <pre class='cython line score-0'>&#xA0;24: </pre>
                        
                        <pre class='cython line score-66' onclick='toggleDiv(this)'>+25:     <span class="k">return</span> <span class="n">np</span><span class="o">.</span><span class="n">array</span><span class="p">(</span><span class="n">minimosx</span><span class="p">),</span> <span class="n">np</span><span class="o">.</span><span class="n">array</span><span class="p">(</span><span class="n">minimosy</span><span class="p">)</span></pre>
                        
                        <pre class='cython code score-66'>  <span class='pyx_macro_api'>__Pyx_XDECREF</span>(__pyx_r);
  __pyx_t_42 = <span class='pyx_c_api'>__Pyx_GetModuleGlobalName</span>(__pyx_n_s_np);<span class='error_goto'> if (unlikely(!__pyx_t_42)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 25; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
  <span class='refnanny'>__Pyx_GOTREF</span>(__pyx_t_42);
  __pyx_t_43 = <span class='pyx_c_api'>__Pyx_PyObject_GetAttrStr</span>(__pyx_t_42, __pyx_n_s_array);<span class='error_goto'> if (unlikely(!__pyx_t_43)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 25; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
  <span class='refnanny'>__Pyx_GOTREF</span>(__pyx_t_43);
  <span class='pyx_macro_api'>__Pyx_DECREF</span>(__pyx_t_42); __pyx_t_42 = 0;
  __pyx_t_42 = NULL;
  if (CYTHON_COMPILING_IN_CPYTHON && unlikely(<span class='py_c_api'>PyMethod_Check</span>(__pyx_t_43))) {
    __pyx_t_42 = <span class='py_macro_api'>PyMethod_GET_SELF</span>(__pyx_t_43);
    if (likely(__pyx_t_42)) {
      PyObject* function = <span class='py_macro_api'>PyMethod_GET_FUNCTION</span>(__pyx_t_43);
      <span class='pyx_macro_api'>__Pyx_INCREF</span>(__pyx_t_42);
      <span class='pyx_macro_api'>__Pyx_INCREF</span>(function);
      <span class='pyx_macro_api'>__Pyx_DECREF_SET</span>(__pyx_t_43, function);
    }
  }
  if (!__pyx_t_42) {
    __pyx_t_1 = <span class='pyx_c_api'>__Pyx_PyObject_CallOneArg</span>(__pyx_t_43, __pyx_v_minimosx);<span class='error_goto'> if (unlikely(!__pyx_t_1)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 25; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
    <span class='refnanny'>__Pyx_GOTREF</span>(__pyx_t_1);
  } else {
    __pyx_t_44 = <span class='py_c_api'>PyTuple_New</span>(1+1);<span class='error_goto'> if (unlikely(!__pyx_t_44)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 25; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
    <span class='refnanny'>__Pyx_GOTREF</span>(__pyx_t_44);
    <span class='py_macro_api'>PyTuple_SET_ITEM</span>(__pyx_t_44, 0, __pyx_t_42); <span class='refnanny'>__Pyx_GIVEREF</span>(__pyx_t_42); __pyx_t_42 = NULL;
    <span class='pyx_macro_api'>__Pyx_INCREF</span>(__pyx_v_minimosx);
    <span class='py_macro_api'>PyTuple_SET_ITEM</span>(__pyx_t_44, 0+1, __pyx_v_minimosx);
    <span class='refnanny'>__Pyx_GIVEREF</span>(__pyx_v_minimosx);
    __pyx_t_1 = <span class='pyx_c_api'>__Pyx_PyObject_Call</span>(__pyx_t_43, __pyx_t_44, NULL);<span class='error_goto'> if (unlikely(!__pyx_t_1)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 25; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
    <span class='refnanny'>__Pyx_GOTREF</span>(__pyx_t_1);
    <span class='pyx_macro_api'>__Pyx_DECREF</span>(__pyx_t_44); __pyx_t_44 = 0;
  }
  <span class='pyx_macro_api'>__Pyx_DECREF</span>(__pyx_t_43); __pyx_t_43 = 0;
  __pyx_t_44 = <span class='pyx_c_api'>__Pyx_GetModuleGlobalName</span>(__pyx_n_s_np);<span class='error_goto'> if (unlikely(!__pyx_t_44)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 25; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
  <span class='refnanny'>__Pyx_GOTREF</span>(__pyx_t_44);
  __pyx_t_42 = <span class='pyx_c_api'>__Pyx_PyObject_GetAttrStr</span>(__pyx_t_44, __pyx_n_s_array);<span class='error_goto'> if (unlikely(!__pyx_t_42)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 25; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
  <span class='refnanny'>__Pyx_GOTREF</span>(__pyx_t_42);
  <span class='pyx_macro_api'>__Pyx_DECREF</span>(__pyx_t_44); __pyx_t_44 = 0;
  __pyx_t_44 = NULL;
  if (CYTHON_COMPILING_IN_CPYTHON && unlikely(<span class='py_c_api'>PyMethod_Check</span>(__pyx_t_42))) {
    __pyx_t_44 = <span class='py_macro_api'>PyMethod_GET_SELF</span>(__pyx_t_42);
    if (likely(__pyx_t_44)) {
      PyObject* function = <span class='py_macro_api'>PyMethod_GET_FUNCTION</span>(__pyx_t_42);
      <span class='pyx_macro_api'>__Pyx_INCREF</span>(__pyx_t_44);
      <span class='pyx_macro_api'>__Pyx_INCREF</span>(function);
      <span class='pyx_macro_api'>__Pyx_DECREF_SET</span>(__pyx_t_42, function);
    }
  }
  if (!__pyx_t_44) {
    __pyx_t_43 = <span class='pyx_c_api'>__Pyx_PyObject_CallOneArg</span>(__pyx_t_42, __pyx_v_minimosy);<span class='error_goto'> if (unlikely(!__pyx_t_43)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 25; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
    <span class='refnanny'>__Pyx_GOTREF</span>(__pyx_t_43);
  } else {
    __pyx_t_45 = <span class='py_c_api'>PyTuple_New</span>(1+1);<span class='error_goto'> if (unlikely(!__pyx_t_45)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 25; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
    <span class='refnanny'>__Pyx_GOTREF</span>(__pyx_t_45);
    <span class='py_macro_api'>PyTuple_SET_ITEM</span>(__pyx_t_45, 0, __pyx_t_44); <span class='refnanny'>__Pyx_GIVEREF</span>(__pyx_t_44); __pyx_t_44 = NULL;
    <span class='pyx_macro_api'>__Pyx_INCREF</span>(__pyx_v_minimosy);
    <span class='py_macro_api'>PyTuple_SET_ITEM</span>(__pyx_t_45, 0+1, __pyx_v_minimosy);
    <span class='refnanny'>__Pyx_GIVEREF</span>(__pyx_v_minimosy);
    __pyx_t_43 = <span class='pyx_c_api'>__Pyx_PyObject_Call</span>(__pyx_t_42, __pyx_t_45, NULL);<span class='error_goto'> if (unlikely(!__pyx_t_43)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 25; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
    <span class='refnanny'>__Pyx_GOTREF</span>(__pyx_t_43);
    <span class='pyx_macro_api'>__Pyx_DECREF</span>(__pyx_t_45); __pyx_t_45 = 0;
  }
  <span class='pyx_macro_api'>__Pyx_DECREF</span>(__pyx_t_42); __pyx_t_42 = 0;
  __pyx_t_42 = <span class='py_c_api'>PyTuple_New</span>(2);<span class='error_goto'> if (unlikely(!__pyx_t_42)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 25; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
  <span class='refnanny'>__Pyx_GOTREF</span>(__pyx_t_42);
  <span class='py_macro_api'>PyTuple_SET_ITEM</span>(__pyx_t_42, 0, __pyx_t_1);
  <span class='refnanny'>__Pyx_GIVEREF</span>(__pyx_t_1);
  <span class='py_macro_api'>PyTuple_SET_ITEM</span>(__pyx_t_42, 1, __pyx_t_43);
  <span class='refnanny'>__Pyx_GIVEREF</span>(__pyx_t_43);
  __pyx_t_1 = 0;
  __pyx_t_43 = 0;
  __pyx_r = ((PyObject*)__pyx_t_42);
  __pyx_t_42 = 0;
  goto __pyx_L0;
</pre>
                      </div>
                      
                      <p>
                        </body></html> </div> </div> </div> </div> </div> 
                        
                        <div>
                          <div>
                          </div>
                          
                          <div>
                            <div>
                              Vemos que muchas de las partes oscuras ahora son más claras!!! Pero parece que sigue quedando espacio para la mejora.</p>
                            </div>
                          </div>
                        </div>
                        
                        <div>
                          <div>
                          </div>
                          
                          <div>
                            <div>
                              <h1 id="Cythonizando,-que-es-gerundio-(toma-5).">
                                Cythonizando, que es gerundio (toma 5).<a class="anchor-link" href="#Cythonizando,-que-es-gerundio-(toma-5).">&#182;</a>
                              </h1>
                            </div>
                          </div>
                        </div>
                        
                        <div>
                          <div>
                          </div>
                          
                          <div>
                            <div>
                              Vamos a ver si definiendo el tipo del resultado de la función como un numpy array en lugar de como una tupla nos introduce alguna mejora:</p>
                            </div>
                          </div>
                        </div>
                        
                        <div>
                          <div>
                            <div>
                              <div>
                                <div class=" highlight hl-ipython3">
                                  <pre><span class="o">%%</span><span class="n">cython</span> <span class="o">--</span><span class="n">name</span> <span class="n">probandocython5</span>
<span class="k">import</span> <span class="nn">numpy</span> <span class="k">as</span> <span class="nn">np</span>
<span class="k">cimport</span> <span class="nn">numpy</span> <span class="k">as</span> <span class="nn">np</span>

<span class="k">cpdef</span> <span class="kt">np</span>.<span class="kt">ndarray</span>[<span class="nf">int</span><span class="p">,</span> <span class="nf">ndim</span> <span class="o">=</span> <span class="mf">2</span><span class="p">]</span> <span class="n">busca_min_cython5</span><span class="p">(</span><span class="n">np</span><span class="o">.</span><span class="n">ndarray</span><span class="p">[</span><span class="n">double</span><span class="p">,</span> <span class="n">ndim</span> <span class="o">=</span> <span class="mf">2</span><span class="p">]</span> <span class="n">malla</span><span class="p">):</span>
    <span class="k">cdef</span> <span class="kt">list</span> <span class="nf">minimosx</span><span class="p">,</span> <span class="nf">minimosy</span>
    <span class="k">cdef</span> <span class="kt">unsigned</span> <span class="kt">int</span> <span class="nf">i</span><span class="p">,</span> <span class="nf">j</span>
    <span class="k">cdef</span> <span class="kt">unsigned</span> <span class="kt">int</span> <span class="nf">ii</span> <span class="o">=</span> <span class="n">malla</span><span class="o">.</span><span class="n">shape</span><span class="p">[</span><span class="mf">1</span><span class="p">]</span><span class="o">-</span><span class="mf">1</span>
    <span class="k">cdef</span> <span class="kt">unsigned</span> <span class="kt">int</span> <span class="nf">jj</span> <span class="o">=</span> <span class="n">malla</span><span class="o">.</span><span class="n">shape</span><span class="p">[</span><span class="mf"></span><span class="p">]</span><span class="o">-</span><span class="mf">1</span>
    <span class="k">cdef</span> <span class="kt">unsigned</span> <span class="kt">int</span> <span class="nf">start</span> <span class="o">=</span> <span class="mf">1</span>
    <span class="n">minimosx</span> <span class="o">=</span> <span class="p">[]</span>
    <span class="n">minimosy</span> <span class="o">=</span> <span class="p">[]</span>
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

    <span class="k">return</span> <span class="n">np</span><span class="o">.</span><span class="n">array</span><span class="p">([</span><span class="n">minimosx</span><span class="p">,</span> <span class="n">minimosy</span><span class="p">])</span>
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
                                  <pre><span class="o">%</span><span class="k">timeit</span> busca_min_cython5(data)
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
                                  <pre>10 loops, best of 3: 137 ms per loop
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
                              Vaya, parece que con respecto a la versión anterior solo obtenemos una ganancia de un 2% - 4%.</p>
                            </div>
                          </div>
                        </div>
                        
                        <div>
                          <div>
                          </div>
                          
                          <div>
                            <div>
                              <h1 id="Cythonizando,-que-es-gerundio-(toma-6).">
                                Cythonizando, que es gerundio (toma 6).<a class="anchor-link" href="#Cythonizando,-que-es-gerundio-(toma-6).">&#182;</a>
                              </h1>
                            </div>
                          </div>
                        </div>
                        
                        <div>
                          <div>
                          </div>
                          
                          <div>
                            <div>
                              Vamos a dejar de usar listas y vamos a usar numpy arrays vacios que iremos 'rellenando' con <code>numpy.append</code>. A ver si usando todo numpy arrays conseguimos algún tipo de mejora:</p>
                            </div>
                          </div>
                        </div>
                        
                        <div>
                          <div>
                            <div>
                              <div>
                                <div class=" highlight hl-ipython3">
                                  <pre><span class="o">%%</span><span class="n">cython</span> <span class="o">--</span><span class="n">name</span> <span class="n">probandocython6</span>
<span class="k">import</span> <span class="nn">numpy</span> <span class="k">as</span> <span class="nn">np</span>
<span class="k">cimport</span> <span class="nn">numpy</span> <span class="k">as</span> <span class="nn">np</span>

<span class="k">cpdef</span> <span class="kt">tuple</span> <span class="nf">busca_min_cython6</span><span class="p">(</span><span class="n">np</span><span class="o">.</span><span class="n">ndarray</span><span class="p">[</span><span class="n">double</span><span class="p">,</span> <span class="n">ndim</span> <span class="o">=</span> <span class="mf">2</span><span class="p">]</span> <span class="n">malla</span><span class="p">):</span>
    <span class="k">cdef</span> <span class="kt">np</span>.<span class="kt">ndarray</span>[<span class="nf">long</span><span class="p">,</span> <span class="nf">ndim</span> <span class="o">=</span> <span class="mf">1</span><span class="p">]</span> <span class="n">minimosx</span><span class="p">,</span> <span class="n">minimosy</span>
    <span class="k">cdef</span> <span class="kt">unsigned</span> <span class="kt">int</span> <span class="nf">i</span><span class="p">,</span> <span class="nf">j</span>
    <span class="k">cdef</span> <span class="kt">unsigned</span> <span class="kt">int</span> <span class="nf">ii</span> <span class="o">=</span> <span class="n">malla</span><span class="o">.</span><span class="n">shape</span><span class="p">[</span><span class="mf">1</span><span class="p">]</span><span class="o">-</span><span class="mf">1</span>
    <span class="k">cdef</span> <span class="kt">unsigned</span> <span class="kt">int</span> <span class="nf">jj</span> <span class="o">=</span> <span class="n">malla</span><span class="o">.</span><span class="n">shape</span><span class="p">[</span><span class="mf"></span><span class="p">]</span><span class="o">-</span><span class="mf">1</span>
    <span class="k">cdef</span> <span class="kt">unsigned</span> <span class="kt">int</span> <span class="nf">start</span> <span class="o">=</span> <span class="mf">1</span>
    <span class="n">minimosx</span> <span class="o">=</span> <span class="n">np</span><span class="o">.</span><span class="n">array</span><span class="p">([],</span> <span class="n">dtype</span> <span class="o">=</span> <span class="n">np</span><span class="o">.</span><span class="n">int</span><span class="p">)</span>
    <span class="n">minimosy</span> <span class="o">=</span> <span class="n">np</span><span class="o">.</span><span class="n">array</span><span class="p">([],</span> <span class="n">dtype</span> <span class="o">=</span> <span class="n">np</span><span class="o">.</span><span class="n">int</span><span class="p">)</span>
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
                <span class="n">np</span><span class="o">.</span><span class="n">append</span><span class="p">(</span><span class="n">minimosx</span><span class="p">,</span> <span class="n">i</span><span class="p">)</span>
                <span class="n">np</span><span class="o">.</span><span class="n">append</span><span class="p">(</span><span class="n">minimosy</span><span class="p">,</span> <span class="n">j</span><span class="p">)</span>

    <span class="k">return</span> <span class="n">minimosx</span><span class="p">,</span> <span class="n">minimosy</span>
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
                                  <pre><span class="o">%</span><span class="k">timeit</span> busca_min_cython6(data)
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
                                  <pre>1 loops, best of 3: 5.59 s per loop
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
                                  <pre><span class="n">np</span><span class="o">.</span><span class="n">append</span><span class="o">?</span>
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
                              En realidad, en la anterior porción de código estoy usando algo muy ineficiente. La función <code>numpy.append</code> no funciona como una lista a la que vas anexando elementos. Lo que estamos haciendo en realidad es crear copias del array existente para convertirlo a un nuevo array con un elemento nuevo. Esto no es lo que pretendiamos!!!!</p>
                            </div>
                          </div>
                        </div>
                        
                        <div>
                          <div>
                          </div>
                          
                          <div>
                            <div>
                              <h1 id="Cythonizando,-que-es-gerundio-(toma-7).">
                                Cythonizando, que es gerundio (toma 7).<a class="anchor-link" href="#Cythonizando,-que-es-gerundio-(toma-7).">&#182;</a>
                              </h1>
                            </div>
                          </div>
                        </div>
                        
                        <div>
                          <div>
                          </div>
                          
                          <div>
                            <div>
                              En Python existen <a href="https://docs.python.org/3.4/library/array.html">arrays</a> eficientes para valores numéricos (según reza la documentación) que también pueden ser usados de la forma en que estoy usando las listas en mi función (arrays vacios a los que les vamos añadiendo elementos). Vamos a usarlos con Cython.</p>
                            </div>
                          </div>
                        </div>
                        
                        <div>
                          <div>
                            <div>
                              <div>
                                <div class=" highlight hl-ipython3">
                                  <pre><span class="o">%%</span><span class="n">cython</span> <span class="o">--</span><span class="n">name</span> <span class="n">probandocython7</span>
<span class="k">import</span> <span class="nn">numpy</span> <span class="k">as</span> <span class="nn">np</span>
<span class="k">cimport</span> <span class="nn">numpy</span> <span class="k">as</span> <span class="nn">np</span>
<span class="k">from</span> <span class="nn">cpython</span> <span class="k">cimport</span> <span class="n">array</span> <span class="k">as</span> <span class="n">c_array</span>
<span class="k">from</span> <span class="nn">array</span> <span class="k">import</span> <span class="n">array</span>

<span class="k">cpdef</span> <span class="kt">tuple</span> <span class="nf">busca_min_cython7</span><span class="p">(</span><span class="n">np</span><span class="o">.</span><span class="n">ndarray</span><span class="p">[</span><span class="n">double</span><span class="p">,</span> <span class="n">ndim</span> <span class="o">=</span> <span class="mf">2</span><span class="p">]</span> <span class="n">malla</span><span class="p">):</span>
    <span class="k">cdef</span> <span class="kt">c_array</span>.<span class="kt">array</span> <span class="nf">minimosx</span><span class="p">,</span> <span class="nf">minimosy</span>
    <span class="k">cdef</span> <span class="kt">unsigned</span> <span class="kt">int</span> <span class="nf">i</span><span class="p">,</span> <span class="nf">j</span>
    <span class="k">cdef</span> <span class="kt">unsigned</span> <span class="kt">int</span> <span class="nf">ii</span> <span class="o">=</span> <span class="n">malla</span><span class="o">.</span><span class="n">shape</span><span class="p">[</span><span class="mf">1</span><span class="p">]</span><span class="o">-</span><span class="mf">1</span>
    <span class="k">cdef</span> <span class="kt">unsigned</span> <span class="kt">int</span> <span class="nf">jj</span> <span class="o">=</span> <span class="n">malla</span><span class="o">.</span><span class="n">shape</span><span class="p">[</span><span class="mf"></span><span class="p">]</span><span class="o">-</span><span class="mf">1</span>
    <span class="k">cdef</span> <span class="kt">unsigned</span> <span class="kt">int</span> <span class="nf">start</span> <span class="o">=</span> <span class="mf">1</span>
    <span class="n">minimosx</span> <span class="o">=</span> <span class="n">array</span><span class="p">(</span><span class="s">&#39;L&#39;</span><span class="p">,</span> <span class="p">[])</span>
    <span class="n">minimosy</span> <span class="o">=</span> <span class="n">array</span><span class="p">(</span><span class="s">&#39;L&#39;</span><span class="p">,</span> <span class="p">[])</span> 
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
                                  <pre><span class="o">%</span><span class="k">timeit</span> busca_min_cython7(data)
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
                                  <pre>10 loops, best of 3: 98.1 ms per loop
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
                              Parece que hemos ganado otro 25% - 30% con respecto a lo anterior más eficiente que habíamos conseguido. Con respecto a la implementación inicial en Python puro tenemos una mejora de 30x - 35x veces la velocidad inicial.<br /> Vamos a comprobar si seguimos teniendo los mismos resultados.</p>
                            </div>
                          </div>
                        </div>
                        
                        <div>
                          <div>
                            <div>
                              <div>
                                <div class=" highlight hl-ipython3">
                                  <pre><span class="n">a</span><span class="p">,</span> <span class="n">b</span> <span class="o">=</span> <span class="n">busca_min</span><span class="p">(</span><span class="n">data</span><span class="p">)</span>
<span class="nb">print</span><span class="p">(</span><span class="n">a</span><span class="p">)</span>
<span class="nb">print</span><span class="p">(</span><span class="n">b</span><span class="p">)</span>
<span class="n">aa</span><span class="p">,</span> <span class="n">bb</span> <span class="o">=</span> <span class="n">busca_min_cython7</span><span class="p">(</span><span class="n">data</span><span class="p">)</span>
<span class="nb">print</span><span class="p">(</span><span class="n">aa</span><span class="p">)</span>
<span class="nb">print</span><span class="p">(</span><span class="n">bb</span><span class="p">)</span>
<span class="nb">print</span><span class="p">(</span><span class="n">np</span><span class="o">.</span><span class="n">array_equal</span><span class="p">(</span><span class="n">a</span><span class="p">,</span> <span class="n">aa</span><span class="p">))</span>
<span class="nb">print</span><span class="p">(</span><span class="n">np</span><span class="o">.</span><span class="n">array_equal</span><span class="p">(</span><span class="n">b</span><span class="p">,</span> <span class="n">bb</span><span class="p">))</span>
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
                                  <pre>[   1    1    1 ..., 1998 1998 1998]
[   1    3   11 ..., 1968 1977 1985]
[   1    1    1 ..., 1998 1998 1998]
[   1    3   11 ..., 1968 1977 1985]
True
True
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
                              ¿Qué pasa si el tamaño del array se incrementa?</p>
                            </div>
                          </div>
                        </div>
                        
                        <div>
                          <div>
                            <div>
                              <div>
                                <div class=" highlight hl-ipython3">
                                  <pre><span class="n">data2</span> <span class="o">=</span> <span class="n">np</span><span class="o">.</span><span class="n">random</span><span class="o">.</span><span class="n">randn</span><span class="p">(</span><span class="mi">5000</span><span class="p">,</span> <span class="mi">5000</span><span class="p">)</span>
<span class="o">%</span><span class="k">timeit</span> busca_min(data2)
<span class="o">%</span><span class="k">timeit</span> busca_min_cython7(data2)
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
                                  <pre>1 loops, best of 3: 24.6 s per loop
1 loops, best of 3: 687 ms per loop
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
                                  <pre><span class="n">a</span><span class="p">,</span> <span class="n">b</span> <span class="o">=</span> <span class="n">busca_min</span><span class="p">(</span><span class="n">data2</span><span class="p">)</span>
<span class="nb">print</span><span class="p">(</span><span class="n">a</span><span class="p">)</span>
<span class="nb">print</span><span class="p">(</span><span class="n">b</span><span class="p">)</span>
<span class="n">aa</span><span class="p">,</span> <span class="n">bb</span> <span class="o">=</span> <span class="n">busca_min_cython7</span><span class="p">(</span><span class="n">data2</span><span class="p">)</span>
<span class="nb">print</span><span class="p">(</span><span class="n">aa</span><span class="p">)</span>
<span class="nb">print</span><span class="p">(</span><span class="n">bb</span><span class="p">)</span>
<span class="nb">print</span><span class="p">(</span><span class="n">np</span><span class="o">.</span><span class="n">array_equal</span><span class="p">(</span><span class="n">a</span><span class="p">,</span> <span class="n">aa</span><span class="p">))</span>
<span class="nb">print</span><span class="p">(</span><span class="n">np</span><span class="o">.</span><span class="n">array_equal</span><span class="p">(</span><span class="n">b</span><span class="p">,</span> <span class="n">bb</span><span class="p">))</span>
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
                                  <pre>[   1    1    1 ..., 4998 4998 4998]
[   7   12   18 ..., 4975 4978 4983]
[   1    1    1 ..., 4998 4998 4998]
[   7   12   18 ..., 4975 4978 4983]
True
True
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
                              Parece que al ir aumentando el tamaño de los datos de entrada a la función los números son consistentes y el rendimiento se mantiene. En este caso concreto parece que ya hemos llegado a rendimientos de más de ¡¡35x!! con respecto a la implementación inicial.</p>
                            </div>
                          </div>
                        </div>
                        
                        <div>
                          <div>
                          </div>
                          
                          <div>
                            <div>
                              <h1 id="Cythonizando,-que-es-gerundio-(toma-8).">
                                Cythonizando, que es gerundio (toma 8).<a class="anchor-link" href="#Cythonizando,-que-es-gerundio-(toma-8).">&#182;</a>
                              </h1>
                            </div>
                          </div>
                        </div>
                        
                        <div>
                          <div>
                          </div>
                          
                          <div>
                            <div>
                              Podemos usar <a href="http://docs.cython.org/src/reference/compilation.html#compiler-directives">directivas de compilación</a> que ayuden al compilador a decidir mejor qué es lo que tiene que hacer. Entre ellas se encuentra una opción que es <code>boundscheck</code> que evita mirar la posibilidad de obtener <code>IndexError</code> asumiendo que el código está libre de estos errores de indexación. Lo vamos a usar conjuntamente con <code>wraparound</code>. Esta última opción se encarga de evitar mirar indexaciones relativas al final del iterable (por ejemplo, <code>mi_iterable[-1]</code>). En este caso concreto, la segunda opción no aporta nada de mejora de rendimiento pero la dijamos ya que la hemos probado.</p>
                            </div>
                          </div>
                        </div>
                        
                        <div>
                          <div>
                            <div>
                              <div>
                                <div class=" highlight hl-ipython3">
                                  <pre><span class="o">%%</span><span class="n">cython</span> <span class="o">--</span><span class="n">name</span> <span class="n">probandocython8</span>
<span class="k">import</span> <span class="nn">numpy</span> <span class="k">as</span> <span class="nn">np</span>
<span class="k">cimport</span> <span class="nn">numpy</span> <span class="k">as</span> <span class="nn">np</span>
<span class="k">from</span> <span class="nn">cpython</span> <span class="k">cimport</span> <span class="n">array</span> <span class="k">as</span> <span class="n">c_array</span>
<span class="k">from</span> <span class="nn">array</span> <span class="k">import</span> <span class="n">array</span>
<span class="k">cimport</span> <span class="nn">cython</span>

<span class="nd">@cython</span><span class="o">.</span><span class="n">boundscheck</span><span class="p">(</span><span class="bp">False</span><span class="p">)</span> 
<span class="nd">@cython</span><span class="o">.</span><span class="n">wraparound</span><span class="p">(</span><span class="bp">False</span><span class="p">)</span>
<span class="k">cpdef</span> <span class="kt">tuple</span> <span class="nf">busca_min_cython8</span><span class="p">(</span><span class="n">np</span><span class="o">.</span><span class="n">ndarray</span><span class="p">[</span><span class="n">double</span><span class="p">,</span> <span class="n">ndim</span> <span class="o">=</span> <span class="mf">2</span><span class="p">]</span> <span class="n">malla</span><span class="p">):</span>
    <span class="k">cdef</span> <span class="kt">c_array</span>.<span class="kt">array</span> <span class="nf">minimosx</span><span class="p">,</span> <span class="nf">minimosy</span>
    <span class="k">cdef</span> <span class="kt">unsigned</span> <span class="kt">int</span> <span class="nf">i</span><span class="p">,</span> <span class="nf">j</span>
    <span class="k">cdef</span> <span class="kt">unsigned</span> <span class="kt">int</span> <span class="nf">ii</span> <span class="o">=</span> <span class="n">malla</span><span class="o">.</span><span class="n">shape</span><span class="p">[</span><span class="mf">1</span><span class="p">]</span><span class="o">-</span><span class="mf">1</span>
    <span class="k">cdef</span> <span class="kt">unsigned</span> <span class="kt">int</span> <span class="nf">jj</span> <span class="o">=</span> <span class="n">malla</span><span class="o">.</span><span class="n">shape</span><span class="p">[</span><span class="mf"></span><span class="p">]</span><span class="o">-</span><span class="mf">1</span>
    <span class="k">cdef</span> <span class="kt">unsigned</span> <span class="kt">int</span> <span class="nf">start</span> <span class="o">=</span> <span class="mf">1</span>
    <span class="n">minimosx</span> <span class="o">=</span> <span class="n">array</span><span class="p">(</span><span class="s">&#39;L&#39;</span><span class="p">,</span> <span class="p">[])</span>
    <span class="n">minimosy</span> <span class="o">=</span> <span class="n">array</span><span class="p">(</span><span class="s">&#39;L&#39;</span><span class="p">,</span> <span class="p">[])</span> 
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
                                  <pre><span class="o">%</span><span class="k">timeit</span> busca_min_cython8(data)
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
                                  <pre>10 loops, best of 3: 94.3 ms per loop
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
                              Parece que hemos conseguido arañar otro poquito de rendimiento.</p>
                            </div>
                          </div>
                        </div>
                        
                        <div>
                          <div>
                          </div>
                          
                          <div>
                            <div>
                              <h1 id="Cythonizando,-que-es-gerundio-(toma-9).">
                                Cythonizando, que es gerundio (toma 9).<a class="anchor-link" href="#Cythonizando,-que-es-gerundio-(toma-9).">&#182;</a>
                              </h1>
                            </div>
                          </div>
                        </div>
                        
                        <div>
                          <div>
                          </div>
                          
                          <div>
                            <div>
                              En lugar de usar numpy arrays vamos a usar <a href="http://docs.cython.org/src/userguide/memoryviews.html#typed-memoryviews"><em>memoryviews</em></a>. Los <em>memoryviews</em> son arrays de acceso rápido. Si solo queremos almacenar cosas y no necesitamos ninguna de las características de un numpy array pueden ser una buena solución. Si necesitamos alguna funcionalidad extra siempre lo podemos convertir en un numpy array usando <code>numpy.asarray</code>.</p>
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
<span class="c">#cpdef tuple busca_min_cython9(np.ndarray[double, ndim = 2] malla):</span>
<span class="k">cpdef</span> <span class="kt">tuple</span> <span class="nf">busca_min_cython9</span><span class="p">(</span><span class="n">double</span> <span class="p">[:,:]</span> <span class="n">malla</span><span class="p">):</span>
    <span class="k">cdef</span> <span class="kt">c_array</span>.<span class="kt">array</span> <span class="nf">minimosx</span><span class="p">,</span> <span class="nf">minimosy</span>
    <span class="k">cdef</span> <span class="kt">unsigned</span> <span class="kt">int</span> <span class="nf">i</span><span class="p">,</span> <span class="nf">j</span>
    <span class="k">cdef</span> <span class="kt">unsigned</span> <span class="kt">int</span> <span class="nf">ii</span> <span class="o">=</span> <span class="n">malla</span><span class="o">.</span><span class="n">shape</span><span class="p">[</span><span class="mf">1</span><span class="p">]</span><span class="o">-</span><span class="mf">1</span>
    <span class="k">cdef</span> <span class="kt">unsigned</span> <span class="kt">int</span> <span class="nf">jj</span> <span class="o">=</span> <span class="n">malla</span><span class="o">.</span><span class="n">shape</span><span class="p">[</span><span class="mf"></span><span class="p">]</span><span class="o">-</span><span class="mf">1</span>
    <span class="k">cdef</span> <span class="kt">unsigned</span> <span class="kt">int</span> <span class="nf">start</span> <span class="o">=</span> <span class="mf">1</span>
    <span class="c">#cdef float [:, :] malla_view = malla</span>
    <span class="n">minimosx</span> <span class="o">=</span> <span class="n">array</span><span class="p">(</span><span class="s">&#39;L&#39;</span><span class="p">,</span> <span class="p">[])</span>
    <span class="n">minimosy</span> <span class="o">=</span> <span class="n">array</span><span class="p">(</span><span class="s">&#39;L&#39;</span><span class="p">,</span> <span class="p">[])</span> 
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
                                  <pre>10 loops, best of 3: 97.6 ms per loop
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
                              Parece que, virtualmente, el rendimiento es parecido a lo que ya teniamos por lo que parece que nos hemos quedado igual.</p>
                            </div>
                          </div>
                        </div>
                        
                        <div>
                          <div>
                          </div>
                          
                          <div>
                            <div>
                              <h1 id="Bonus-track">
                                Bonus track<a class="anchor-link" href="#Bonus-track">&#182;</a>
                              </h1>
                            </div>
                          </div>
                        </div>
                        
                        <div>
                          <div>
                          </div>
                          
                          <div>
                            <div>
                              Voy a intentar usar pypy (2.4 (CPython 2.7)) conjuntamente con numpypy para ver lo que conseguimos.</p>
                            </div>
                          </div>
                        </div>
                        
                        <div>
                          <div>
                            <div>
                              <div>
                                <div class=" highlight hl-ipython3">
                                  <pre><span class="o">%%</span><span class="k">pypy</span>
import numpy as np
import time

np.random.seed(0)
data = np.random.randn(2000,2000)

def busca_min(malla):
    minimosx = []
    minimosy = []
    for i in range(1, malla.shape[1]-1):
        for j in range(1, malla.shape[0]-1):
            if (malla[j, i] &lt; malla[j-1, i-1] and
                malla[j, i] &lt; malla[j-1, i] and
                malla[j, i] &lt; malla[j-1, i+1] and
                malla[j, i] &lt; malla[j, i-1] and
                malla[j, i] &lt; malla[j, i+1] and
                malla[j, i] &lt; malla[j+1, i-1] and
                malla[j, i] &lt; malla[j+1, i] and
                malla[j, i] &lt; malla[j+1, i+1]):
                minimosx.append(i)
                minimosy.append(j)

    return np.array(minimosx), np.array(minimosy)

resx, resy = busca_min(data)
print(data)
print(len(resx), len(resy))
print(resx)
print(resy)

t = []
for i in range(100):
    t0 = time.time()
    busca_min(data)
    t1 = time.time() - t0
    t.append(t1)
print(sum(t) / 100.)
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
                                  <pre>[[ 1.76405235  0.40015721  0.97873798 ...,  0.15843385 -1.14190142
  -1.31097037]
 [-1.53292105 -1.71197016  0.04613506 ..., -0.03057244  1.57708821
  -0.8128021 ]
 [ 0.61334917  1.84369998  0.27109098 ..., -0.53788475  0.39344443
   0.28651827]
 ..., 
 [-0.17117027  0.57332063 -0.89516715 ..., -0.01409412  1.28756456
  -0.6953778 ]
 [-1.53627571  0.57441228 -0.20564476 ...,  0.90499929  0.51428298
   0.72148202]
 [ 0.51262101 -0.90758583  1.78121159 ..., -1.12554283  0.95170926
  -1.15237806]]
(443641, 443641)
[   1    1    1 ..., 1998 1998 1998]
[   1    3   11 ..., 1968 1977 1985]
0.3795211339
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
                              El último valor del output anterior es el tiempo promedio después de repetir el cálculo 100 veces.<br /> Wow!! Parece que sin hacer modificaciones tenemos que el resultado es 10x - 15x veces más rápido que el obtenido usando la función inicial. Y llega a ser solo 3.5x veces más lento que lo que hemos conseguido con Cython.</p>
                            </div>
                          </div>
                        </div>
                        
                        <div>
                          <div>
                          </div>
                          
                          <div>
                            <div>
                              <h1 id="Resumen-de-resultados.">
                                Resumen de resultados.<a class="anchor-link" href="#Resumen-de-resultados.">&#182;</a>
                              </h1>
                            </div>
                          </div>
                        </div>
                        
                        <div>
                          <div>
                          </div>
                          
                          <div>
                            <div>
                              Vamos a ver los resultados completos en un breve resumen. Primero vamos a ver los tiempos de las diferentes versiones de la función <code>busca_min_xxx</code>:</p>
                            </div>
                          </div>
                        </div>
                        
                        <div>
                          <div>
                            <div>
                              <div>
                                <div class=" highlight hl-ipython3">
                                  <pre><span class="n">funcs</span> <span class="o">=</span> <span class="p">[</span><span class="n">busca_min</span><span class="p">,</span> <span class="n">busca_min_numba</span><span class="p">,</span> <span class="n">busca_min_cython1</span><span class="p">,</span>
         <span class="n">busca_min_cython2</span><span class="p">,</span> <span class="n">busca_min_cython3</span><span class="p">,</span>
         <span class="n">busca_min_cython4</span><span class="p">,</span> <span class="n">busca_min_cython5</span><span class="p">,</span>
         <span class="n">busca_min_cython6</span><span class="p">,</span> <span class="n">busca_min_cython7</span><span class="p">,</span>
         <span class="n">busca_min_cython8</span><span class="p">,</span> <span class="n">busca_min_cython9</span><span class="p">]</span>
<span class="n">t</span> <span class="o">=</span> <span class="p">[]</span>
<span class="k">for</span> <span class="n">func</span> <span class="ow">in</span> <span class="n">funcs</span><span class="p">:</span>
    <span class="n">res</span> <span class="o">=</span> <span class="o">%</span><span class="k">timeit</span> -o func(data)
    <span class="n">t</span><span class="o">.</span><span class="n">append</span><span class="p">(</span><span class="n">res</span><span class="o">.</span><span class="n">best</span><span class="p">)</span>
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
                                  <pre>1 loops, best of 3: 3.67 s per loop
1 loops, best of 3: 5.34 s per loop
1 loops, best of 3: 3.41 s per loop
1 loops, best of 3: 3.54 s per loop
1 loops, best of 3: 3.65 s per loop
10 loops, best of 3: 139 ms per loop
10 loops, best of 3: 136 ms per loop
1 loops, best of 3: 5.65 s per loop
10 loops, best of 3: 95.4 ms per loop
10 loops, best of 3: 89 ms per loop
10 loops, best of 3: 92.3 ms per loop
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
                                  <pre><span class="n">index</span> <span class="o">=</span> <span class="n">np</span><span class="o">.</span><span class="n">arange</span><span class="p">(</span><span class="nb">len</span><span class="p">(</span><span class="n">t</span><span class="p">))</span>
<span class="n">plt</span><span class="o">.</span><span class="n">figure</span><span class="p">(</span><span class="n">figsize</span> <span class="o">=</span> <span class="p">(</span><span class="mi">12</span><span class="p">,</span> <span class="mi">6</span><span class="p">))</span>
<span class="n">plt</span><span class="o">.</span><span class="n">bar</span><span class="p">(</span><span class="n">index</span><span class="p">,</span> <span class="n">t</span><span class="p">)</span>
<span class="n">plt</span><span class="o">.</span><span class="n">xticks</span><span class="p">(</span><span class="n">index</span> <span class="o">+</span> <span class="mf">0.4</span><span class="p">,</span> <span class="p">[</span><span class="n">func</span><span class="o">.</span><span class="n">__name__</span><span class="p">[</span><span class="mi">9</span><span class="p">:]</span> <span class="k">for</span> <span class="n">func</span> <span class="ow">in</span> <span class="n">funcs</span><span class="p">])</span>
<span class="n">plt</span><span class="o">.</span><span class="n">tight_layout</span><span class="p">()</span>
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
                                  <img src="http://pybonacci.org/wp-content/uploads/2015/03/wpid-C_elemental_querido_Cython1.png"
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
                              En el gráfico anterior, la primera barra corresponde a la función de partida (<code>busca_min</code>). Recordemos que la versión de pypy ha tardado unos 0.38 segundos.</p>
                            </div>
                          </div>
                        </div>
                        
                        <div>
                          <div>
                          </div>
                          
                          <div>
                            <div>
                              Y ahora vamos a ver los tiempos entre <code>busca_min</code> (la versión original) y la última versión de cython que hemos creado, <code>busca_min_cython9</code> usando diferentes tamaños de la matriz de entrada:</p>
                            </div>
                          </div>
                        </div>
                        
                        <div>
                          <div>
                            <div>
                              <div>
                                <div class=" highlight hl-ipython3">
                                  <pre><span class="n">tamanyos</span> <span class="o">=</span> <span class="p">[</span><span class="mi">10</span><span class="p">,</span> <span class="mi">100</span><span class="p">,</span> <span class="mi">500</span><span class="p">,</span> <span class="mi">1000</span><span class="p">,</span> <span class="mi">2000</span><span class="p">,</span> <span class="mi">5000</span><span class="p">]</span>
<span class="n">t_p</span> <span class="o">=</span> <span class="p">[]</span>
<span class="n">t_c</span> <span class="o">=</span> <span class="p">[]</span>
<span class="k">for</span> <span class="n">i</span> <span class="ow">in</span> <span class="n">tamanyos</span><span class="p">:</span>
    <span class="n">data</span> <span class="o">=</span> <span class="n">np</span><span class="o">.</span><span class="n">random</span><span class="o">.</span><span class="n">randn</span><span class="p">(</span><span class="n">i</span><span class="p">,</span> <span class="n">i</span><span class="p">)</span>
    <span class="n">res</span> <span class="o">=</span> <span class="o">%</span><span class="k">timeit</span> -o busca_min(data)
    <span class="n">t_p</span><span class="o">.</span><span class="n">append</span><span class="p">(</span><span class="n">res</span><span class="o">.</span><span class="n">best</span><span class="p">)</span>
    <span class="n">res</span> <span class="o">=</span> <span class="o">%</span><span class="k">timeit</span> -o busca_min_cython9(data)
    <span class="n">t_c</span><span class="o">.</span><span class="n">append</span><span class="p">(</span><span class="n">res</span><span class="o">.</span><span class="n">best</span><span class="p">)</span>
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
                                  <pre>10000 loops, best of 3: 67.9 µs per loop
The slowest run took 4.77 times longer than the fastest. This could mean that an intermediate result is being cached 
100000 loops, best of 3: 5.13 µs per loop
100 loops, best of 3: 8.65 ms per loop
10000 loops, best of 3: 177 µs per loop
1 loops, best of 3: 223 ms per loop
100 loops, best of 3: 5.51 ms per loop
1 loops, best of 3: 890 ms per loop
10 loops, best of 3: 26.6 ms per loop
1 loops, best of 3: 3.64 s per loop
10 loops, best of 3: 92.8 ms per loop
1 loops, best of 3: 22.8 s per loop
1 loops, best of 3: 605 ms per loop
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
                                  <pre><span class="n">plt</span><span class="o">.</span><span class="n">figure</span><span class="p">(</span><span class="n">figsize</span> <span class="o">=</span> <span class="p">(</span><span class="mi">10</span><span class="p">,</span><span class="mi">6</span><span class="p">))</span>
<span class="n">plt</span><span class="o">.</span><span class="n">plot</span><span class="p">(</span><span class="n">tamanyos</span><span class="p">,</span> <span class="n">t_p</span><span class="p">,</span> <span class="s">&#39;bo-&#39;</span><span class="p">)</span>
<span class="n">plt</span><span class="o">.</span><span class="n">plot</span><span class="p">(</span><span class="n">tamanyos</span><span class="p">,</span> <span class="n">t_c</span><span class="p">,</span> <span class="s">&#39;ro-&#39;</span><span class="p">)</span>
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
                                  <pre>[&lt;matplotlib.lines.Line2D at 0x7f5b810a1d30&gt;]</pre>
                                </div>
                              </div>
                              
                              <div>
                                <div>
                                </div>
                                
                                <div>
                                  <img src="http://pybonacci.org/wp-content/uploads/2015/03/wpid-C_elemental_querido_Cython2.png"
 />
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
                                  <pre><span class="n">ratio</span> <span class="o">=</span> <span class="n">np</span><span class="o">.</span><span class="n">array</span><span class="p">(</span><span class="n">t_p</span><span class="p">)</span> <span class="o">/</span> <span class="n">np</span><span class="o">.</span><span class="n">array</span><span class="p">(</span><span class="n">t_c</span><span class="p">)</span>
<span class="n">plt</span><span class="o">.</span><span class="n">figure</span><span class="p">(</span><span class="n">figsize</span> <span class="o">=</span> <span class="p">(</span><span class="mi">10</span><span class="p">,</span><span class="mi">6</span><span class="p">))</span>
<span class="n">plt</span><span class="o">.</span><span class="n">plot</span><span class="p">(</span><span class="n">tamanyos</span><span class="p">,</span> <span class="n">ratio</span><span class="p">,</span> <span class="s">&#39;bo-&#39;</span><span class="p">)</span>
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
                                  <pre>[&lt;matplotlib.lines.Line2D at 0x7f5b810af2e8&gt;]</pre>
                                </div>
                              </div>
                              
                              <div>
                                <div>
                                </div>
                                
                                <div>
                                  <img src="http://pybonacci.org/wp-content/uploads/2015/03/wpid-C_elemental_querido_Cython3.png"
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
                              Parece que conseguimos rendimientos que son 40 veces más rápidos que con Python puro que usa un numpy array de por medio (excepto para tamaños de arrays muy pequeños en los que el rendimiento no sería una gran problema).</p>
                            </div>
                          </div>
                        </div>
                        
                        <div>
                          <div>
                          </div>
                          
                          <div>
                            <div>
                              <h1 id="Apuntes-finales">
                                Apuntes finales<a class="anchor-link" href="#Apuntes-finales">&#182;</a>
                              </h1>
                            </div>
                          </div>
                        </div>
                        
                        <div>
                          <div>
                          </div>
                          
                          <div>
                            <div>
                              Después de haber probado Python, Cython, Numba y Pypy:<br /> <strong>Numba</strong>:</p> 
                              
                              <ul>
                                <li>
                                  Numba no parece fácilmente generalizable a día de hoy (experiencia personal) y no soporta ni parece que soportará todas las características del lenguaje. La idea me parece increible pero creo que le falta todavía un poco de madurez.
                                </li>
                                <li>
                                  Me ha costado instalar numba y llvmlite en linux sin usar conda (con conda no lo he probado por lo que no puedo opinar).
                                </li>
                              </ul>
                              
                              <p>
                                (Creo que JuanLu estaba preparando un post sobre Numba. Habrá que esperar a ver sus conclusiones).<br /> <strong>Pypy</strong>:
                              </p>
                              
                              <ul>
                                <li>
                                  Pypy ha funcionado como un titán sin necesidad de hacer modificaciones.
                                </li>
                                <li>
                                  Destacar que no tengo excesivas experiencias con el mismo
                                </li>
                                <li>
                                  Instalarlo no es tarea fácil (he intentado usar PyPy3 con numpypy y he fallado vilmente). Quería usar numpypy y al final he optado por descargar una versión portable con numpy de serie que quizá afecte al rendimiento ¿?.
                                </li>
                              </ul>
                              
                              <p>
                                <strong>Cython</strong>:
                              </p>
                              
                              <ul>
                                <li>
                                  Me ha parecido el más generalizable de todos. Se pueden crear paquetes para CPython, para Pypy,...
                                </li>
                                <li>
                                  No lo he probado en Windows por lo que no sé lo doloroso que puede llegar a ser. Mañana lo probaré en el trabajo y ya dejaré un comentario por ahí.
                                </li>
                                <li>
                                  El manejo no es tan evidente como con Numba y Pypy. Requiere entender como funcionan los tipos de C y requiere conocer una serie de interioridades de C. Sin duda es el que más esfuerzo requiere de las alternativas aquí expuestas pra este caso concreto y no generalizable.
                                </li>
                                <li>
                                  Creo que, una vez hecho el esfuerzo inicial de intentar entender un poco como funciona, se puede sacar un gran rendimiento del mismo en muchas situaciones.
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
                              Y después de haber leído todo esto pensad que, en la mayoría de situaciones, CPython no es tan lento como lo pintan (sobretodo con numpy) y que ¡¡¡LA OPTIMIZACIÓN PREMATURA ES LA RAÍZ DE TODOS LOS MALES!!!</p>
                            </div>
                          </div>
                        </div>