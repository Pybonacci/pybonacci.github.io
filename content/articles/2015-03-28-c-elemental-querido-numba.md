---
title: C elemental, querido numba
date: 2015-03-28T22:10:45+00:00
author: Kiko Correoso
slug: c-elemental-querido-numba
tags: blttlenec, cython, numba, numbagg, numpy, python, rendimiento

<div>
  <div>
  </div>
  
  <div>
    <div>
      <h2 id="Volvemos-al-torneo-del-rendimiento!!!">
        Volvemos al torneo del rendimiento!!!<a class="anchor-link" href="#Volvemos-al-torneo-del-rendimiento!!!">&#182;</a>
      </h2>
    </div>
  </div>
</div>

<div>
  <div>
  </div>
  
  <div>
    <div>
      Recapitulando. Un artículo sobre Cython donde conseguíamos <a href="http://pybonacci.org/2015/03/09/c-elemental-querido-cython/">mejoras de velocidad de código Python con numpy arrays de 40x usando Cython</a> desembocó <a href="http://pybonacci.org/2015/03/13/como-acelerar-tu-codigo-python-con-numba/">en mejoras de 70x usando numba</a>. En esta tercera toma vamos a ver si con Cython conseguimos las velocidades de numba tomando algunas ideas de la implementación de JuanLu y definiendo una función un poco más inteligente que mi implementación con Cython (<a href="http://pybonacci.org/2015/03/09/c-elemental-querido-cython/#Cythonizando,-que-es-gerundio-%28toma-9%29.">busca_min_cython9</a>).</p>
    </div>
  </div>
</div>

<div>
  <div>
  </div>
  
  <div>
    <div>
      Preparamos el <em>setup inicial</em>.</p>
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
      JuanLu hizo alguna trampa usando un numpy array en lugar de dos listas y devolviendo el resultado usando <code>numpy.nonzero</code>. En realidad no es trampa, es pura envidia mía al ver que ha usado una forma más inteligente de conseguir lo mismo que hacía mi función original 😛<br /> Usando esa implementación considero que es más inteligente tener un numpy array de salida por lo que el uso de <code>np.nonzero</code> sería innecesario y añadiría algo de pérdida de rendimiento si luego vamos a seguir trabajando con numpy arrays. Por tanto, la implementación de JuanLu eliminando el uso de <code>numpy.nonzero</code> sería:</p>
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
    <span class="k">return</span> <span class="n">minimos</span>  <span class="c"># en lugar de &#39;return np.nonzero(minimos)&#39;</span>

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
    <div>
      <div>
        <div class=" highlight hl-ipython3">
          <pre><span class="o">%</span><span class="k">timeit</span> -n 100 busca_min_np_jit(data)
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
          <pre>100 loops, best of 3: 33 ms per loop
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
      Ejecutándolo 100 veces obtenemos un valor más bajo de 33.6 ms devolviendo un numpy.array de 1's y 0's con los 1's indicando la posición de los máximos.<br /> La implementación original la vamos a modificar un poco para que devuelva lo mismo.</p>
    </div>
  </div>
</div>

<div>
  <div>
    <div>
      <div>
        <div class=" highlight hl-ipython3">
          <pre><span class="k">def</span> <span class="nf">busca_min</span><span class="p">(</span><span class="n">malla</span><span class="p">):</span>
    <span class="n">minimos</span> <span class="o">=</span> <span class="n">np</span><span class="o">.</span><span class="n">zeros_like</span><span class="p">(</span><span class="n">malla</span><span class="p">)</span>
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
                <span class="n">minimos</span><span class="p">[</span><span class="n">i</span><span class="p">,</span> <span class="n">j</span><span class="p">]</span> <span class="o">=</span> <span class="mi">1</span>

    <span class="k">return</span> <span class="n">minimos</span>
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
          <pre>1 loops, best of 3: 3.4 s per loop
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
      Los tiempos son similares a la función original y, aunque estamos usando más memoria, tenemos una mejora con numba que ya llega a los dos órdenes de magnitud (alrededor de 100x!!) y una función más usable para trabajar con numpy.</p>
    </div>
  </div>
</div>

<div>
  <div>
  </div>
  
  <div>
    <div>
      Vamos a modificar la opción Cython más rápida que obtuvimos para que se comporte igual que las de Numba y Python.<br /> Primero cargamos la extensión Cython.</p>
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
      Vamos a usar la opción <code>annotate</code> para ver cuanto 'blanco' tenemos y la nueva versión Cython la vamos a llamar <code>busca_min_cython10</code>.</p>
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
<span class="k">from</span> <span class="nn">cython</span> <span class="k">cimport</span> <span class="n">boundscheck</span><span class="p">,</span> <span class="n">wraparound</span>

<span class="k">cpdef</span> <span class="kt">char</span>[<span class="p">:,::</span><span class="mf">1</span><span class="p">]</span> <span class="n">busca_min_cython10</span><span class="p">(</span><span class="n">double</span><span class="p">[:,</span> <span class="p">::</span><span class="mf">1</span><span class="p">]</span> <span class="n">malla</span><span class="p">):</span>
    <span class="k">cdef</span> <span class="kt">unsigned</span> <span class="kt">int</span> <span class="nf">i</span><span class="p">,</span> <span class="nf">j</span>
    <span class="k">cdef</span> <span class="kt">unsigned</span> <span class="kt">int</span> <span class="nf">ii</span> <span class="o">=</span> <span class="n">malla</span><span class="o">.</span><span class="n">shape</span><span class="p">[</span><span class="mf">1</span><span class="p">]</span><span class="o">-</span><span class="mf">1</span>
    <span class="k">cdef</span> <span class="kt">unsigned</span> <span class="kt">int</span> <span class="nf">jj</span> <span class="o">=</span> <span class="n">malla</span><span class="o">.</span><span class="n">shape</span><span class="p">[</span><span class="mf"></span><span class="p">]</span><span class="o">-</span><span class="mf">1</span>
    <span class="k">cdef</span> <span class="kt">char</span>[<span class="p">:,::</span><span class="mf">1</span><span class="p">]</span> <span class="n">minimos</span> <span class="o">=</span> <span class="n">np</span><span class="o">.</span><span class="n">zeros_like</span><span class="p">(</span><span class="n">malla</span><span class="p">,</span> <span class="n">dtype</span> <span class="o">=</span> <span class="n">np</span><span class="o">.</span><span class="n">int8</span><span class="p">)</span>
    <span class="c">#minimos[...] = 0</span>
    <span class="k">cdef</span> <span class="kt">unsigned</span> <span class="kt">int</span> <span class="nf">start</span> <span class="o">=</span> <span class="mf">1</span>
    <span class="c">#cdef float [:, :] malla_view = malla</span>
    <span class="k">with</span> <span class="n">boundscheck</span><span class="p">(</span><span class="bp">False</span><span class="p">),</span> <span class="n">wraparound</span><span class="p">(</span><span class="bp">False</span><span class="p">):</span>
        <span class="k">for</span> <span class="n">j</span> <span class="ow">in</span> <span class="nb">range</span><span class="p">(</span><span class="n">start</span><span class="p">,</span> <span class="n">ii</span><span class="p">):</span>
            <span class="k">for</span> <span class="n">i</span> <span class="ow">in</span> <span class="nb">range</span><span class="p">(</span><span class="n">start</span><span class="p">,</span> <span class="n">jj</span><span class="p">):</span>
                <span class="k">if</span> <span class="p">(</span><span class="n">malla</span><span class="p">[</span><span class="n">j</span><span class="p">,</span> <span class="n">i</span><span class="p">]</span> <span class="o">&lt;</span> <span class="n">malla</span><span class="p">[</span><span class="n">j</span><span class="o">-</span><span class="mf">1</span><span class="p">,</span> <span class="n">i</span><span class="o">-</span><span class="mf">1</span><span class="p">]</span> <span class="ow">and</span>
                    <span class="n">malla</span><span class="p">[</span><span class="n">j</span><span class="p">,</span> <span class="n">i</span><span class="p">]</span> <span class="o">&lt;</span> <span class="n">malla</span><span class="p">[</span><span class="n">j</span><span class="o">-</span><span class="mf">1</span><span class="p">,</span> <span class="n">i</span><span class="p">]</span> <span class="ow">and</span>
                    <span class="n">malla</span><span class="p">[</span><span class="n">j</span><span class="p">,</span> <span class="n">i</span><span class="p">]</span> <span class="o">&lt;</span> <span class="n">malla</span><span class="p">[</span><span class="n">j</span><span class="o">-</span><span class="mf">1</span><span class="p">,</span> <span class="n">i</span><span class="o">+</span><span class="mf">1</span><span class="p">]</span> <span class="ow">and</span>
                    <span class="n">malla</span><span class="p">[</span><span class="n">j</span><span class="p">,</span> <span class="n">i</span><span class="p">]</span> <span class="o">&lt;</span> <span class="n">malla</span><span class="p">[</span><span class="n">j</span><span class="p">,</span> <span class="n">i</span><span class="o">-</span><span class="mf">1</span><span class="p">]</span> <span class="ow">and</span>
                    <span class="n">malla</span><span class="p">[</span><span class="n">j</span><span class="p">,</span> <span class="n">i</span><span class="p">]</span> <span class="o">&lt;</span> <span class="n">malla</span><span class="p">[</span><span class="n">j</span><span class="p">,</span> <span class="n">i</span><span class="o">+</span><span class="mf">1</span><span class="p">]</span> <span class="ow">and</span>
                    <span class="n">malla</span><span class="p">[</span><span class="n">j</span><span class="p">,</span> <span class="n">i</span><span class="p">]</span> <span class="o">&lt;</span> <span class="n">malla</span><span class="p">[</span><span class="n">j</span><span class="o">+</span><span class="mf">1</span><span class="p">,</span> <span class="n">i</span><span class="o">-</span><span class="mf">1</span><span class="p">]</span> <span class="ow">and</span>
                    <span class="n">malla</span><span class="p">[</span><span class="n">j</span><span class="p">,</span> <span class="n">i</span><span class="p">]</span> <span class="o">&lt;</span> <span class="n">malla</span><span class="p">[</span><span class="n">j</span><span class="o">+</span><span class="mf">1</span><span class="p">,</span> <span class="n">i</span><span class="p">]</span> <span class="ow">and</span>
                    <span class="n">malla</span><span class="p">[</span><span class="n">j</span><span class="p">,</span> <span class="n">i</span><span class="p">]</span> <span class="o">&lt;</span> <span class="n">malla</span><span class="p">[</span><span class="n">j</span><span class="o">+</span><span class="mf">1</span><span class="p">,</span> <span class="n">i</span><span class="o">+</span><span class="mf">1</span><span class="p">]):</span>
                    <span class="n">minimos</span><span class="p">[</span><span class="n">i</span><span class="p">,</span><span class="n">j</span><span class="p">]</span> <span class="o">=</span> <span class="mf">1</span>

    <span class="k">return</span> <span class="n">minimos</span>
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
            
            <pre class='cython line score-0'>&#xA0;02: <span class="k">from</span> <span class="nn">cython</span> <span class="k">cimport</span> <span class="n">boundscheck</span><span class="p">,</span> <span class="n">wraparound</span></pre>
            
            <pre class='cython line score-0'>&#xA0;03: </pre>
            
            <pre class='cython line score-22' onclick='toggleDiv(this)'>+04: <span class="k">cpdef</span> <span class="kt">char</span>[<span class="p">:,::</span><span class="mf">1</span><span class="p">]</span> <span class="n">busca_min_cython10</span><span class="p">(</span><span class="n">double</span><span class="p">[:,</span> <span class="p">::</span><span class="mf">1</span><span class="p">]</span> <span class="n">malla</span><span class="p">):</span></pre>
            
            <pre class='cython code score-22'>static PyObject *__pyx_pw_46_cython_magic_de7594aedda59602146d5e749862b110_1busca_min_cython10(PyObject *__pyx_self, PyObject *__pyx_arg_malla); /*proto*/
static __Pyx_memviewslice __pyx_f_46_cython_magic_de7594aedda59602146d5e749862b110_busca_min_cython10(__Pyx_memviewslice __pyx_v_malla, CYTHON_UNUSED int __pyx_skip_dispatch) {
  unsigned int __pyx_v_i;
  unsigned int __pyx_v_j;
  unsigned int __pyx_v_ii;
  unsigned int __pyx_v_jj;
  __Pyx_memviewslice __pyx_v_minimos = { 0, 0, { 0 }, { 0 }, { 0 } };
  unsigned int __pyx_v_start;
  __Pyx_memviewslice __pyx_r = { 0, 0, { 0 }, { 0 }, { 0 } };
  <span class='refnanny'>__Pyx_RefNannyDeclarations</span>
  <span class='refnanny'>__Pyx_RefNannySetupContext</span>("busca_min_cython10", 0);
/* … */
  /* function exit code */
  __pyx_L1_error:;
  <span class='pyx_macro_api'>__Pyx_XDECREF</span>(__pyx_t_1);
  <span class='pyx_macro_api'>__Pyx_XDECREF</span>(__pyx_t_2);
  <span class='pyx_macro_api'>__Pyx_XDECREF</span>(__pyx_t_3);
  <span class='pyx_macro_api'>__Pyx_XDECREF</span>(__pyx_t_4);
  <span class='pyx_macro_api'>__Pyx_XDECREF</span>(__pyx_t_5);
  __PYX_XDEC_MEMVIEW(&__pyx_t_6, 1);
  __pyx_r.data = NULL;
  __pyx_r.memview = NULL;
  <span class='pyx_c_api'>__Pyx_AddTraceback</span>("_cython_magic_de7594aedda59602146d5e749862b110.busca_min_cython10", __pyx_clineno, __pyx_lineno, __pyx_filename);

  goto __pyx_L2;
  __pyx_L0:;
  if (unlikely(!__pyx_r.memview)) {
    <span class='py_c_api'>PyErr_SetString</span>(PyExc_TypeError,"Memoryview return value is not initialized");
  }
  __pyx_L2:;
  __PYX_XDEC_MEMVIEW(&__pyx_v_minimos, 1);
  <span class='refnanny'>__Pyx_RefNannyFinishContext</span>();
  return __pyx_r;
}

/* Python wrapper */
static PyObject *__pyx_pw_46_cython_magic_de7594aedda59602146d5e749862b110_1busca_min_cython10(PyObject *__pyx_self, PyObject *__pyx_arg_malla); /*proto*/
static PyObject *__pyx_pw_46_cython_magic_de7594aedda59602146d5e749862b110_1busca_min_cython10(PyObject *__pyx_self, PyObject *__pyx_arg_malla) {
  __Pyx_memviewslice __pyx_v_malla = { 0, 0, { 0 }, { 0 }, { 0 } };
  PyObject *__pyx_r = 0;
  <span class='refnanny'>__Pyx_RefNannyDeclarations</span>
  <span class='refnanny'>__Pyx_RefNannySetupContext</span>("busca_min_cython10 (wrapper)", 0);
  assert(__pyx_arg_malla); {
    __pyx_v_malla = <span class='pyx_c_api'>__Pyx_PyObject_to_MemoryviewSlice_d_dc_double</span>(__pyx_arg_malla);<span class='error_goto'> if (unlikely(!__pyx_v_malla.memview)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 4; __pyx_clineno = __LINE__; goto __pyx_L3_error;}</span>
  }
  goto __pyx_L4_argument_unpacking_done;
  __pyx_L3_error:;
  <span class='pyx_c_api'>__Pyx_AddTraceback</span>("_cython_magic_de7594aedda59602146d5e749862b110.busca_min_cython10", __pyx_clineno, __pyx_lineno, __pyx_filename);
  <span class='refnanny'>__Pyx_RefNannyFinishContext</span>();
  return NULL;
  __pyx_L4_argument_unpacking_done:;
  __pyx_r = __pyx_pf_46_cython_magic_de7594aedda59602146d5e749862b110_busca_min_cython10(__pyx_self, __pyx_v_malla);
  int __pyx_lineno = 0;
  const char *__pyx_filename = NULL;
  int __pyx_clineno = 0;

  /* function exit code */
  <span class='refnanny'>__Pyx_RefNannyFinishContext</span>();
  return __pyx_r;
}

static PyObject *__pyx_pf_46_cython_magic_de7594aedda59602146d5e749862b110_busca_min_cython10(CYTHON_UNUSED PyObject *__pyx_self, __Pyx_memviewslice __pyx_v_malla) {
  PyObject *__pyx_r = NULL;
  <span class='refnanny'>__Pyx_RefNannyDeclarations</span>
  <span class='refnanny'>__Pyx_RefNannySetupContext</span>("busca_min_cython10", 0);
  <span class='pyx_macro_api'>__Pyx_XDECREF</span>(__pyx_r);
  if (unlikely(!__pyx_v_malla.memview)) { <span class='pyx_c_api'>__Pyx_RaiseUnboundLocalError</span>("malla"); <span class='error_goto'>{__pyx_filename = __pyx_f[0]; __pyx_lineno = 4; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span> }
  __pyx_t_1 = __pyx_f_46_cython_magic_de7594aedda59602146d5e749862b110_busca_min_cython10(__pyx_v_malla, 0);<span class='error_goto'> if (unlikely(!__pyx_t_1.memview)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 4; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
  __pyx_t_2 = __pyx_memoryview_fromslice(__pyx_t_1, 2, (PyObject *(*)(char *)) __pyx_memview_get_char, (int (*)(char *, PyObject *)) __pyx_memview_set_char, 0);;<span class='error_goto'> if (unlikely(!__pyx_t_2)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 4; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
  <span class='refnanny'>__Pyx_GOTREF</span>(__pyx_t_2);
  __PYX_XDEC_MEMVIEW(&__pyx_t_1, 1);
  __pyx_r = __pyx_t_2;
  __pyx_t_2 = 0;
  goto __pyx_L0;

  /* function exit code */
  __pyx_L1_error:;
  __PYX_XDEC_MEMVIEW(&__pyx_t_1, 1);
  <span class='pyx_macro_api'>__Pyx_XDECREF</span>(__pyx_t_2);
  <span class='pyx_c_api'>__Pyx_AddTraceback</span>("_cython_magic_de7594aedda59602146d5e749862b110.busca_min_cython10", __pyx_clineno, __pyx_lineno, __pyx_filename);
  __pyx_r = NULL;
  __pyx_L0:;
  __PYX_XDEC_MEMVIEW(&__pyx_v_malla, 1);
  <span class='refnanny'>__Pyx_XGIVEREF</span>(__pyx_r);
  <span class='refnanny'>__Pyx_RefNannyFinishContext</span>();
  return __pyx_r;
}
</pre>
            
            <pre class='cython line score-0'>&#xA0;05:     <span class="k">cdef</span> <span class="kt">unsigned</span> <span class="kt">int</span> <span class="nf">i</span><span class="p">,</span> <span class="nf">j</span></pre>
            
            <pre class='cython line score-0' onclick='toggleDiv(this)'>+06:     <span class="k">cdef</span> <span class="kt">unsigned</span> <span class="kt">int</span> <span class="nf">ii</span> <span class="o">=</span> <span class="n">malla</span><span class="o">.</span><span class="n">shape</span><span class="p">[</span><span class="mf">1</span><span class="p">]</span><span class="o">-</span><span class="mf">1</span></pre>
            
            <pre class='cython code score-0'>  __pyx_v_ii = ((__pyx_v_malla.shape[1]) - 1);
</pre>
            
            <pre class='cython line score-0' onclick='toggleDiv(this)'>+07:     <span class="k">cdef</span> <span class="kt">unsigned</span> <span class="kt">int</span> <span class="nf">jj</span> <span class="o">=</span> <span class="n">malla</span><span class="o">.</span><span class="n">shape</span><span class="p">[</span><span class="mf"></span><span class="p">]</span><span class="o">-</span><span class="mf">1</span></pre>
            
            <pre class='cython code score-0'>  __pyx_v_jj = ((__pyx_v_malla.shape[0]) - 1);
</pre>
            
            <pre class='cython line score-35' onclick='toggleDiv(this)'>+08:     <span class="k">cdef</span> <span class="kt">char</span>[<span class="p">:,::</span><span class="mf">1</span><span class="p">]</span> <span class="n">minimos</span> <span class="o">=</span> <span class="n">np</span><span class="o">.</span><span class="n">zeros_like</span><span class="p">(</span><span class="n">malla</span><span class="p">,</span> <span class="n">dtype</span> <span class="o">=</span> <span class="n">np</span><span class="o">.</span><span class="n">int8</span><span class="p">)</span></pre>
            
            <pre class='cython code score-35'>  __pyx_t_1 = <span class='pyx_c_api'>__Pyx_GetModuleGlobalName</span>(__pyx_n_s_np);<span class='error_goto'> if (unlikely(!__pyx_t_1)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 8; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
  <span class='refnanny'>__Pyx_GOTREF</span>(__pyx_t_1);
  __pyx_t_2 = <span class='pyx_c_api'>__Pyx_PyObject_GetAttrStr</span>(__pyx_t_1, __pyx_n_s_zeros_like);<span class='error_goto'> if (unlikely(!__pyx_t_2)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 8; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
  <span class='refnanny'>__Pyx_GOTREF</span>(__pyx_t_2);
  <span class='pyx_macro_api'>__Pyx_DECREF</span>(__pyx_t_1); __pyx_t_1 = 0;
  __pyx_t_1 = __pyx_memoryview_fromslice(__pyx_v_malla, 2, (PyObject *(*)(char *)) __pyx_memview_get_double, (int (*)(char *, PyObject *)) __pyx_memview_set_double, 0);;<span class='error_goto'> if (unlikely(!__pyx_t_1)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 8; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
  <span class='refnanny'>__Pyx_GOTREF</span>(__pyx_t_1);
  __pyx_t_3 = <span class='py_c_api'>PyTuple_New</span>(1);<span class='error_goto'> if (unlikely(!__pyx_t_3)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 8; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
  <span class='refnanny'>__Pyx_GOTREF</span>(__pyx_t_3);
  <span class='py_macro_api'>PyTuple_SET_ITEM</span>(__pyx_t_3, 0, __pyx_t_1);
  <span class='refnanny'>__Pyx_GIVEREF</span>(__pyx_t_1);
  __pyx_t_1 = 0;
  __pyx_t_1 = <span class='py_c_api'>PyDict_New</span>();<span class='error_goto'> if (unlikely(!__pyx_t_1)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 8; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
  <span class='refnanny'>__Pyx_GOTREF</span>(__pyx_t_1);
  __pyx_t_4 = <span class='pyx_c_api'>__Pyx_GetModuleGlobalName</span>(__pyx_n_s_np);<span class='error_goto'> if (unlikely(!__pyx_t_4)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 8; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
  <span class='refnanny'>__Pyx_GOTREF</span>(__pyx_t_4);
  __pyx_t_5 = <span class='pyx_c_api'>__Pyx_PyObject_GetAttrStr</span>(__pyx_t_4, __pyx_n_s_int8);<span class='error_goto'> if (unlikely(!__pyx_t_5)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 8; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
  <span class='refnanny'>__Pyx_GOTREF</span>(__pyx_t_5);
  <span class='pyx_macro_api'>__Pyx_DECREF</span>(__pyx_t_4); __pyx_t_4 = 0;
  if (<span class='py_c_api'>PyDict_SetItem</span>(__pyx_t_1, __pyx_n_s_dtype, __pyx_t_5) &lt; 0) <span class='error_goto'>{__pyx_filename = __pyx_f[0]; __pyx_lineno = 8; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
  <span class='pyx_macro_api'>__Pyx_DECREF</span>(__pyx_t_5); __pyx_t_5 = 0;
  __pyx_t_5 = <span class='pyx_c_api'>__Pyx_PyObject_Call</span>(__pyx_t_2, __pyx_t_3, __pyx_t_1);<span class='error_goto'> if (unlikely(!__pyx_t_5)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 8; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
  <span class='refnanny'>__Pyx_GOTREF</span>(__pyx_t_5);
  <span class='pyx_macro_api'>__Pyx_DECREF</span>(__pyx_t_2); __pyx_t_2 = 0;
  <span class='pyx_macro_api'>__Pyx_DECREF</span>(__pyx_t_3); __pyx_t_3 = 0;
  <span class='pyx_macro_api'>__Pyx_DECREF</span>(__pyx_t_1); __pyx_t_1 = 0;
  __pyx_t_6 = <span class='pyx_c_api'>__Pyx_PyObject_to_MemoryviewSlice_d_dc_char</span>(__pyx_t_5);
  if (unlikely(!__pyx_t_6.memview)) <span class='error_goto'>{__pyx_filename = __pyx_f[0]; __pyx_lineno = 8; __pyx_clineno = __LINE__; goto __pyx_L1_error;}</span>
  <span class='pyx_macro_api'>__Pyx_DECREF</span>(__pyx_t_5); __pyx_t_5 = 0;
  __pyx_v_minimos = __pyx_t_6;
  __pyx_t_6.memview = NULL;
  __pyx_t_6.data = NULL;
</pre>
            
            <pre class='cython line score-0'>&#xA0;09:     <span class="c">#minimos[...] = 0</span></pre>
            
            <pre class='cython line score-0' onclick='toggleDiv(this)'>+10:     <span class="k">cdef</span> <span class="kt">unsigned</span> <span class="kt">int</span> <span class="nf">start</span> <span class="o">=</span> <span class="mf">1</span></pre>
            
            <pre class='cython code score-0'>  __pyx_v_start = 1;
</pre>
            
            <pre class='cython line score-0'>&#xA0;11:     <span class="c">#cdef float [:, :] malla_view = malla</span></pre>
            
            <pre class='cython line score-0'>&#xA0;12:     <span class="k">with</span> <span class="n">boundscheck</span><span class="p">(</span><span class="bp">False</span><span class="p">),</span> <span class="n">wraparound</span><span class="p">(</span><span class="bp">False</span><span class="p">):</span></pre>
            
            <pre class='cython line score-0' onclick='toggleDiv(this)'>+13:         <span class="k">for</span> <span class="n">j</span> <span class="ow">in</span> <span class="nb">range</span><span class="p">(</span><span class="n">start</span><span class="p">,</span> <span class="n">ii</span><span class="p">):</span></pre>
            
            <pre class='cython code score-0'>  __pyx_t_7 = __pyx_v_ii;
  for (__pyx_t_8 = __pyx_v_start; __pyx_t_8 &lt; __pyx_t_7; __pyx_t_8+=1) {
    __pyx_v_j = __pyx_t_8;
</pre>
            
            <pre class='cython line score-0' onclick='toggleDiv(this)'>+14:             <span class="k">for</span> <span class="n">i</span> <span class="ow">in</span> <span class="nb">range</span><span class="p">(</span><span class="n">start</span><span class="p">,</span> <span class="n">jj</span><span class="p">):</span></pre>
            
            <pre class='cython code score-0'>    __pyx_t_9 = __pyx_v_jj;
    for (__pyx_t_10 = __pyx_v_start; __pyx_t_10 &lt; __pyx_t_9; __pyx_t_10+=1) {
      __pyx_v_i = __pyx_t_10;
</pre>
            
            <pre class='cython line score-0' onclick='toggleDiv(this)'>+15:                 <span class="k">if</span> <span class="p">(</span><span class="n">malla</span><span class="p">[</span><span class="n">j</span><span class="p">,</span> <span class="n">i</span><span class="p">]</span> <span class="o">&lt;</span> <span class="n">malla</span><span class="p">[</span><span class="n">j</span><span class="o">-</span><span class="mf">1</span><span class="p">,</span> <span class="n">i</span><span class="o">-</span><span class="mf">1</span><span class="p">]</span> <span class="ow">and</span></pre>
            
            <pre class='cython code score-0'>      __pyx_t_12 = __pyx_v_j;
      __pyx_t_13 = __pyx_v_i;
      __pyx_t_14 = (__pyx_v_j - 1);
      __pyx_t_15 = (__pyx_v_i - 1);
      __pyx_t_16 = (((*((double *) ( /* dim=1 */ ((char *) (((double *) ( /* dim=0 */ (__pyx_v_malla.data + __pyx_t_12 * __pyx_v_malla.strides[0]) )) + __pyx_t_13)) ))) &lt; (*((double *) ( /* dim=1 */ ((char *) (((double *) ( /* dim=0 */ (__pyx_v_malla.data + __pyx_t_14 * __pyx_v_malla.strides[0]) )) + __pyx_t_15)) )))) != 0);
      if (__pyx_t_16) {
      } else {
        __pyx_t_11 = __pyx_t_16;
        goto __pyx_L8_bool_binop_done;
      }
</pre>
            
            <pre class='cython line score-0' onclick='toggleDiv(this)'>+16:                     <span class="n">malla</span><span class="p">[</span><span class="n">j</span><span class="p">,</span> <span class="n">i</span><span class="p">]</span> <span class="o">&lt;</span> <span class="n">malla</span><span class="p">[</span><span class="n">j</span><span class="o">-</span><span class="mf">1</span><span class="p">,</span> <span class="n">i</span><span class="p">]</span> <span class="ow">and</span></pre>
            
            <pre class='cython code score-0'>      __pyx_t_17 = __pyx_v_j;
      __pyx_t_18 = __pyx_v_i;
      __pyx_t_19 = (__pyx_v_j - 1);
      __pyx_t_20 = __pyx_v_i;
      __pyx_t_16 = (((*((double *) ( /* dim=1 */ ((char *) (((double *) ( /* dim=0 */ (__pyx_v_malla.data + __pyx_t_17 * __pyx_v_malla.strides[0]) )) + __pyx_t_18)) ))) &lt; (*((double *) ( /* dim=1 */ ((char *) (((double *) ( /* dim=0 */ (__pyx_v_malla.data + __pyx_t_19 * __pyx_v_malla.strides[0]) )) + __pyx_t_20)) )))) != 0);
      if (__pyx_t_16) {
      } else {
        __pyx_t_11 = __pyx_t_16;
        goto __pyx_L8_bool_binop_done;
      }
</pre>
            
            <pre class='cython line score-0' onclick='toggleDiv(this)'>+17:                     <span class="n">malla</span><span class="p">[</span><span class="n">j</span><span class="p">,</span> <span class="n">i</span><span class="p">]</span> <span class="o">&lt;</span> <span class="n">malla</span><span class="p">[</span><span class="n">j</span><span class="o">-</span><span class="mf">1</span><span class="p">,</span> <span class="n">i</span><span class="o">+</span><span class="mf">1</span><span class="p">]</span> <span class="ow">and</span></pre>
            
            <pre class='cython code score-0'>      __pyx_t_21 = __pyx_v_j;
      __pyx_t_22 = __pyx_v_i;
      __pyx_t_23 = (__pyx_v_j - 1);
      __pyx_t_24 = (__pyx_v_i + 1);
      __pyx_t_16 = (((*((double *) ( /* dim=1 */ ((char *) (((double *) ( /* dim=0 */ (__pyx_v_malla.data + __pyx_t_21 * __pyx_v_malla.strides[0]) )) + __pyx_t_22)) ))) &lt; (*((double *) ( /* dim=1 */ ((char *) (((double *) ( /* dim=0 */ (__pyx_v_malla.data + __pyx_t_23 * __pyx_v_malla.strides[0]) )) + __pyx_t_24)) )))) != 0);
      if (__pyx_t_16) {
      } else {
        __pyx_t_11 = __pyx_t_16;
        goto __pyx_L8_bool_binop_done;
      }
</pre>
            
            <pre class='cython line score-0' onclick='toggleDiv(this)'>+18:                     <span class="n">malla</span><span class="p">[</span><span class="n">j</span><span class="p">,</span> <span class="n">i</span><span class="p">]</span> <span class="o">&lt;</span> <span class="n">malla</span><span class="p">[</span><span class="n">j</span><span class="p">,</span> <span class="n">i</span><span class="o">-</span><span class="mf">1</span><span class="p">]</span> <span class="ow">and</span></pre>
            
            <pre class='cython code score-0'>      __pyx_t_25 = __pyx_v_j;
      __pyx_t_26 = __pyx_v_i;
      __pyx_t_27 = __pyx_v_j;
      __pyx_t_28 = (__pyx_v_i - 1);
      __pyx_t_16 = (((*((double *) ( /* dim=1 */ ((char *) (((double *) ( /* dim=0 */ (__pyx_v_malla.data + __pyx_t_25 * __pyx_v_malla.strides[0]) )) + __pyx_t_26)) ))) &lt; (*((double *) ( /* dim=1 */ ((char *) (((double *) ( /* dim=0 */ (__pyx_v_malla.data + __pyx_t_27 * __pyx_v_malla.strides[0]) )) + __pyx_t_28)) )))) != 0);
      if (__pyx_t_16) {
      } else {
        __pyx_t_11 = __pyx_t_16;
        goto __pyx_L8_bool_binop_done;
      }
</pre>
            
            <pre class='cython line score-0' onclick='toggleDiv(this)'>+19:                     <span class="n">malla</span><span class="p">[</span><span class="n">j</span><span class="p">,</span> <span class="n">i</span><span class="p">]</span> <span class="o">&lt;</span> <span class="n">malla</span><span class="p">[</span><span class="n">j</span><span class="p">,</span> <span class="n">i</span><span class="o">+</span><span class="mf">1</span><span class="p">]</span> <span class="ow">and</span></pre>
            
            <pre class='cython code score-0'>      __pyx_t_29 = __pyx_v_j;
      __pyx_t_30 = __pyx_v_i;
      __pyx_t_31 = __pyx_v_j;
      __pyx_t_32 = (__pyx_v_i + 1);
      __pyx_t_16 = (((*((double *) ( /* dim=1 */ ((char *) (((double *) ( /* dim=0 */ (__pyx_v_malla.data + __pyx_t_29 * __pyx_v_malla.strides[0]) )) + __pyx_t_30)) ))) &lt; (*((double *) ( /* dim=1 */ ((char *) (((double *) ( /* dim=0 */ (__pyx_v_malla.data + __pyx_t_31 * __pyx_v_malla.strides[0]) )) + __pyx_t_32)) )))) != 0);
      if (__pyx_t_16) {
      } else {
        __pyx_t_11 = __pyx_t_16;
        goto __pyx_L8_bool_binop_done;
      }
</pre>
            
            <pre class='cython line score-0' onclick='toggleDiv(this)'>+20:                     <span class="n">malla</span><span class="p">[</span><span class="n">j</span><span class="p">,</span> <span class="n">i</span><span class="p">]</span> <span class="o">&lt;</span> <span class="n">malla</span><span class="p">[</span><span class="n">j</span><span class="o">+</span><span class="mf">1</span><span class="p">,</span> <span class="n">i</span><span class="o">-</span><span class="mf">1</span><span class="p">]</span> <span class="ow">and</span></pre>
            
            <pre class='cython code score-0'>      __pyx_t_33 = __pyx_v_j;
      __pyx_t_34 = __pyx_v_i;
      __pyx_t_35 = (__pyx_v_j + 1);
      __pyx_t_36 = (__pyx_v_i - 1);
      __pyx_t_16 = (((*((double *) ( /* dim=1 */ ((char *) (((double *) ( /* dim=0 */ (__pyx_v_malla.data + __pyx_t_33 * __pyx_v_malla.strides[0]) )) + __pyx_t_34)) ))) &lt; (*((double *) ( /* dim=1 */ ((char *) (((double *) ( /* dim=0 */ (__pyx_v_malla.data + __pyx_t_35 * __pyx_v_malla.strides[0]) )) + __pyx_t_36)) )))) != 0);
      if (__pyx_t_16) {
      } else {
        __pyx_t_11 = __pyx_t_16;
        goto __pyx_L8_bool_binop_done;
      }
</pre>
            
            <pre class='cython line score-0' onclick='toggleDiv(this)'>+21:                     <span class="n">malla</span><span class="p">[</span><span class="n">j</span><span class="p">,</span> <span class="n">i</span><span class="p">]</span> <span class="o">&lt;</span> <span class="n">malla</span><span class="p">[</span><span class="n">j</span><span class="o">+</span><span class="mf">1</span><span class="p">,</span> <span class="n">i</span><span class="p">]</span> <span class="ow">and</span></pre>
            
            <pre class='cython code score-0'>      __pyx_t_37 = __pyx_v_j;
      __pyx_t_38 = __pyx_v_i;
      __pyx_t_39 = (__pyx_v_j + 1);
      __pyx_t_40 = __pyx_v_i;
      __pyx_t_16 = (((*((double *) ( /* dim=1 */ ((char *) (((double *) ( /* dim=0 */ (__pyx_v_malla.data + __pyx_t_37 * __pyx_v_malla.strides[0]) )) + __pyx_t_38)) ))) &lt; (*((double *) ( /* dim=1 */ ((char *) (((double *) ( /* dim=0 */ (__pyx_v_malla.data + __pyx_t_39 * __pyx_v_malla.strides[0]) )) + __pyx_t_40)) )))) != 0);
      if (__pyx_t_16) {
      } else {
        __pyx_t_11 = __pyx_t_16;
        goto __pyx_L8_bool_binop_done;
      }
</pre>
            
            <pre class='cython line score-0' onclick='toggleDiv(this)'>+22:                     <span class="n">malla</span><span class="p">[</span><span class="n">j</span><span class="p">,</span> <span class="n">i</span><span class="p">]</span> <span class="o">&lt;</span> <span class="n">malla</span><span class="p">[</span><span class="n">j</span><span class="o">+</span><span class="mf">1</span><span class="p">,</span> <span class="n">i</span><span class="o">+</span><span class="mf">1</span><span class="p">]):</span></pre>
            
            <pre class='cython code score-0'>      __pyx_t_41 = __pyx_v_j;
      __pyx_t_42 = __pyx_v_i;
      __pyx_t_43 = (__pyx_v_j + 1);
      __pyx_t_44 = (__pyx_v_i + 1);
      __pyx_t_16 = (((*((double *) ( /* dim=1 */ ((char *) (((double *) ( /* dim=0 */ (__pyx_v_malla.data + __pyx_t_41 * __pyx_v_malla.strides[0]) )) + __pyx_t_42)) ))) &lt; (*((double *) ( /* dim=1 */ ((char *) (((double *) ( /* dim=0 */ (__pyx_v_malla.data + __pyx_t_43 * __pyx_v_malla.strides[0]) )) + __pyx_t_44)) )))) != 0);
      __pyx_t_11 = __pyx_t_16;
      __pyx_L8_bool_binop_done:;
      if (__pyx_t_11) {
</pre>
            
            <pre class='cython line score-0' onclick='toggleDiv(this)'>+23:                     <span class="n">minimos</span><span class="p">[</span><span class="n">i</span><span class="p">,</span><span class="n">j</span><span class="p">]</span> <span class="o">=</span> <span class="mf">1</span></pre>
            
            <pre class='cython code score-0'>        __pyx_t_45 = __pyx_v_i;
        __pyx_t_46 = __pyx_v_j;
        *((char *) ( /* dim=1 */ ((char *) (((char *) ( /* dim=0 */ (__pyx_v_minimos.data + __pyx_t_45 * __pyx_v_minimos.strides[0]) )) + __pyx_t_46)) )) = 1;
        goto __pyx_L7;
      }
      __pyx_L7:;
    }
  }
</pre>
            
            <pre class='cython line score-0'>&#xA0;24: </pre>
            
            <pre class='cython line score-0' onclick='toggleDiv(this)'>+25:     <span class="k">return</span> <span class="n">minimos</span></pre>
            
            <pre class='cython code score-0'>  __PYX_INC_MEMVIEW(&__pyx_v_minimos, 0);
  __pyx_r = __pyx_v_minimos;
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
                  Vemos que la mayor parte está en 'blanco'. Eso significa que estamos evitando usar la C-API de CPython y la mayor parte sucede en C. Estoy usando <code>typed memoryviews</code> que permite trabajar de forma 'transparente' con numpy arrays.<br /> Vamos a ejecutar la nueva versión 100 veces, de la misma forma que hemos hecho con Numba:</p>
                </div>
              </div>
            </div>
            
            <div>
              <div>
                <div>
                  <div>
                    <div class=" highlight hl-ipython3">
                      <pre><span class="o">%</span><span class="k">timeit</span> -n 100 busca_min_cython10(data)
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
                      <pre>100 loops, best of 3: 27.6 ms per loop
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
                  Wow, virtualmente obtenemos la misma velocidad entre Numba y Cython y dos órdenes de magnitud de mejora con respecto a la versión Python.</p>
                </div>
              </div>
            </div>
            
            <div>
              <div>
                <div>
                  <div>
                    <div class=" highlight hl-ipython3">
                      <pre><span class="n">res_numba</span> <span class="o">=</span> <span class="n">busca_min_np_jit</span><span class="p">(</span><span class="n">data</span><span class="p">)</span>
<span class="n">res_cython</span> <span class="o">=</span> <span class="n">busca_min_cython10</span><span class="p">(</span><span class="n">data</span><span class="p">)</span>
<span class="n">res_python</span> <span class="o">=</span> <span class="n">busca_min</span><span class="p">(</span><span class="n">data</span><span class="p">)</span>

<span class="n">np</span><span class="o">.</span><span class="n">testing</span><span class="o">.</span><span class="n">assert_array_equal</span><span class="p">(</span><span class="n">res_numba</span><span class="p">,</span> <span class="n">res_cython</span><span class="p">)</span>
<span class="n">np</span><span class="o">.</span><span class="n">testing</span><span class="o">.</span><span class="n">assert_array_equal</span><span class="p">(</span><span class="n">res_numba</span><span class="p">,</span> <span class="n">res_python</span><span class="p">)</span>
<span class="n">np</span><span class="o">.</span><span class="n">testing</span><span class="o">.</span><span class="n">assert_array_equal</span><span class="p">(</span><span class="n">res_cython</span><span class="p">,</span> <span class="n">res_python</span><span class="p">)</span>
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
                  Parece que el resultado es el mismo en todo momento</p>
                </div>
              </div>
            </div>
            
            <div>
              <div>
              </div>
              
              <div>
                <div>
                  Probemos con arrays de menos y más tamaño.</p>
                </div>
              </div>
            </div>
            
            <div>
              <div>
                <div>
                  <div>
                    <div class=" highlight hl-ipython3">
                      <pre><span class="n">data</span> <span class="o">=</span> <span class="n">np</span><span class="o">.</span><span class="n">random</span><span class="o">.</span><span class="n">randn</span><span class="p">(</span><span class="mi">500</span><span class="p">,</span> <span class="mi">500</span><span class="p">)</span>
<span class="o">%</span><span class="k">timeit</span> -n 3 busca_min_np_jit(data)
<span class="o">%</span><span class="k">timeit</span> -n 3 busca_min_cython10(data)
<span class="o">%</span><span class="k">timeit</span> busca_min(data)
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
                      <pre>3 loops, best of 3: 2.04 ms per loop
3 loops, best of 3: 1.75 ms per loop
1 loops, best of 3: 209 ms per loop
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
                      <pre><span class="n">data</span> <span class="o">=</span> <span class="n">np</span><span class="o">.</span><span class="n">random</span><span class="o">.</span><span class="n">randn</span><span class="p">(</span><span class="mi">5000</span><span class="p">,</span> <span class="mi">5000</span><span class="p">)</span>
<span class="o">%</span><span class="k">timeit</span> -n 3 busca_min_np_jit(data)
<span class="o">%</span><span class="k">timeit</span> -n 3 busca_min_cython10(data)
<span class="o">%</span><span class="k">timeit</span> busca_min(data)
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
                      <pre>3 loops, best of 3: 216 ms per loop
3 loops, best of 3: 174 ms per loop
1 loops, best of 3: 21.6 s per loop
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
                  Parece que las distintas versiones escalan de la misma forma y el rendimiento parece, más o menos, lineal.</p>
                </div>
              </div>
            </div>
            
            <div>
              <div>
              </div>
              
              <div>
                <div>
                  <h2 id="Conclusiones-de-este-nuevo-cap&#237;tulo.">
                    Conclusiones de este nuevo cap&#237;tulo.<a class="anchor-link" href="#Conclusiones-de-este-nuevo-cap&#237;tulo.">&#182;</a>
                  </h2>
                </div>
              </div>
            </div>
            
            <div>
              <div>
              </div>
              
              <div>
                <div>
                  Las conclusiones que saco yo de este mano a mano que hemos llevado a cabo JuanLu (featuring Numba) y yo (featuring Cython):</p> 
                  
                  <ul>
                    <li>
                      Cython: Si te restringes a cosas sencllas, es relativamente sencillo de usar. Básicamente habría que optimizar bucles y, solo en caso de que sea necesario, añadir tipos a otras variables para evitar pasar por la C-API de CPython en ciertas operaciones puesto que puede tener un coste elevado en el rendimiento. Para cosas más complejas, a pesar de que sigue siendo más placentero que C se puede complicar un poco más (pero no mucho más, una vez que has entendido cómo usarlo).
                    </li>
                    <li>
                      Numba: Es bastante sorprendente lo que se puede llegar a conseguir con poco esfuerzo. Parece que siempre introducirá un poco de <em>overhead</em> puesto que hace muchas cosas entre bambalinas y de la otra forma (Cython) hace lo que le digamos que haga. También es verdad que muchas cosas no están soportadas, que los errores que obtenemos puede ser un poco crípticos y se hace difícil depurar el código. Pero a pesar de todo lo anterior y conociendo el historial de la gente que está detrás del proyecto Numba creo que su futuro será brillante. Por ejemplo, <a href="https://github.com/shoyer/numbagg">Numbagg</a> es una librería que usa Numba y que pretende hacer lo mismo que <a href="https://github.com/kwgoodman/bottleneck">bottleneck</a> (una librería muy especializada para determinadas operaciones de Numpy), que usa Cython consiguiendo <a href="https://github.com/shoyer/numbagg#benchmarks">resultados comparables aunque levemente peores</a>.
                    </li>
                  </ul>
                  
                  <p>
                    No sé si habrá algún capítulo más de esta serie... Lo dejo en manos de JuanLu o de cualquiera que nos quiera enviar un nuevo post relacionado.
                  </p>
                </div>
              </div>
            </div>