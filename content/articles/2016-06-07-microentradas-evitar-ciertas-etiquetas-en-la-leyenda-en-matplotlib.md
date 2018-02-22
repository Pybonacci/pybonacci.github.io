---
title: Microentradas: Evitar ciertas etiquetas en la leyenda en Matplotlib
date: 2016-06-07T01:51:59+00:00
author: Kiko Correoso
slug: microentradas-evitar-ciertas-etiquetas-en-la-leyenda-en-matplotlib
tags: labels, Legend, matplotlib, MicroEntradas

<div>
  <p>
    A veces, me llegan ficheros de datos con datos cada hora o cada día y los quiero representar en un <em>plot</em>. Para ello, podría acumular los ficheros en uno solo y luego pintarlo pero como lo debo hacer en 'tiempo casi-real' se puede meter todo en un bucle <code>while</code> que espera los ficheros cada hora/día/lo que sea y va pintando cada variable por tramos. Por ejemplo, una aproximación podría ser la siguiente:
  </p>
</div>

<div>
  <div>
    <div>
      <div>
        <div class=" highlight hl-ipython3">
          <pre><span class="kn">import</span> <span class="nn">numpy</span> <span class="k">as</span> <span class="nn">np</span>
<span class="kn">import</span> <span class="nn">matplotlib.pyplot</span> <span class="k">as</span> <span class="nn">plt</span>
<span class="n">plt</span><span class="o">.</span><span class="n">style</span><span class="o">.</span><span class="n">use</span><span class="p">(</span><span class="s1">'bmh'</span><span class="p">)</span>
<span class="o">%</span><span class="k">matplotlib</span> inline

<span class="n">plt</span><span class="o">.</span><span class="n">figure</span><span class="p">(</span><span class="n">figsize</span> <span class="o">=</span> <span class="p">(</span><span class="mi">12</span><span class="p">,</span> <span class="mi">6</span><span class="p">))</span>
<span class="k">for</span> <span class="n">i</span> <span class="ow">in</span> <span class="nb">range</span><span class="p">(</span><span class="mi">10</span><span class="p">):</span>
    <span class="n">x</span> <span class="o">=</span> <span class="n">np</span><span class="o">.</span><span class="n">arange</span><span class="p">(</span><span class="n">i</span> <span class="o">*</span> <span class="mi">10</span><span class="p">,</span> <span class="n">i</span> <span class="o">*</span> <span class="mi">10</span> <span class="o">+</span> <span class="mi">10</span><span class="p">)</span>
    <span class="n">y_var1</span> <span class="o">=</span> <span class="n">np</span><span class="o">.</span><span class="n">random</span><span class="o">.</span><span class="n">randint</span><span class="p">(</span><span class="mi">1</span><span class="p">,</span> <span class="mi">5</span><span class="p">,</span> <span class="mi">10</span><span class="p">)</span>
    <span class="n">y_var2</span> <span class="o">=</span> <span class="n">np</span><span class="o">.</span><span class="n">random</span><span class="o">.</span><span class="n">randint</span><span class="p">(</span><span class="mi">5</span><span class="p">,</span> <span class="mi">8</span><span class="p">,</span> <span class="mi">10</span><span class="p">)</span>
    <span class="n">plt</span><span class="o">.</span><span class="n">plot</span><span class="p">(</span><span class="n">x</span><span class="p">,</span> <span class="n">y_var1</span><span class="p">,</span> <span class="n">color</span> <span class="o">=</span> <span class="s1">'k'</span><span class="p">,</span> <span class="n">label</span> <span class="o">=</span> <span class="s1">'variable1'</span><span class="p">)</span>
    <span class="n">plt</span><span class="o">.</span><span class="n">plot</span><span class="p">(</span><span class="n">x</span><span class="p">,</span> <span class="n">y_var2</span><span class="p">,</span> <span class="n">color</span> <span class="o">=</span> <span class="s1">'g'</span><span class="p">,</span> <span class="n">label</span> <span class="o">=</span> <span class="s1">'variable2'</span><span class="p">)</span>
    <span class="n">plt</span><span class="o">.</span><span class="n">legend</span><span class="p">()</span>
    <span class="n">plt</span><span class="o">.</span><span class="n">ylim</span><span class="p">(</span><span class="mi"></span><span class="p">,</span> <span class="mi">9</span><span class="p">)</span>
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
          <img src="http://new.pybonacci.org/images/2016/06/wpid-Microentradas_Evitar_ciertas_etiquetas_en_la_leyenda_en_Matplotlib-ipynb1.png" alt="" />
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
        Como véis, en la gráfica anterior hay varios problemas pero como esta es una <a href="http://pybonacci.org/tag/microentradas/">MicroEntrada</a> solo nos vamos a centrar en el problema de las etiquetas repetidas en la leyenda.
      </p>
      
      <h2 id="¿Cómo-podríamos-evitar-el-meter-tantas-veces-una-etiqueta-repetida?">
        ¿Cómo podríamos evitar el meter tantas veces una etiqueta repetida?<a class="anchor-link" href="#¿Cómo-podríamos-evitar-el-meter-tantas-veces-una-etiqueta-repetida?">¶</a>
      </h2>
      
      <p>
        Mi problema es que el bucle es o podría ser 'infinito' y tengo que inicializar las etiquetas de alguna forma. Si miro en esta respuesta encontrada en <a href="http://stackoverflow.com/a/19386045">Stackoverflow</a> dice que en la documentación se indica que <em>"If label attribute is empty string or starts with “_”, those artists will be ignored."</em> pero si busco <a href="http://matplotlib.org/api/artist_api.html#matplotlib.artist.Artist.set_label">aquí</a> o <a href="http://matplotlib.org/users/legend_guide.html">en el enlace que indican en la respuesta en Stackoverflow</a> no veo esa funcionalidad indicada en ningún sitio. Eso es porque aparecía en la versión <a href="https://github.com/matplotlib/matplotlib/blob/v1.3.1/doc/users/legend_guide.rst">1.3.1</a> pero <a href="https://github.com/matplotlib/matplotlib/blob/v1.4.0/doc/users/legend_guide.rst">luego desapareció</a>... Sin embargo podemos seguir usando esa funcionalidad aunque actualmente no esté documentada:
      </p>
    </div>
  </div>
</div>

<div>
  <div>
    <div>
      <div>
        <div class=" highlight hl-ipython3">
          <pre><span class="n">plt</span><span class="o">.</span><span class="n">figure</span><span class="p">(</span><span class="n">figsize</span> <span class="o">=</span> <span class="p">(</span><span class="mi">12</span><span class="p">,</span> <span class="mi">6</span><span class="p">))</span>
<span class="k">for</span> <span class="n">i</span> <span class="ow">in</span> <span class="nb">range</span><span class="p">(</span><span class="mi">10</span><span class="p">):</span>
    <span class="n">x</span> <span class="o">=</span> <span class="n">np</span><span class="o">.</span><span class="n">arange</span><span class="p">(</span><span class="n">i</span> <span class="o">*</span> <span class="mi">10</span><span class="p">,</span> <span class="n">i</span> <span class="o">*</span> <span class="mi">10</span> <span class="o">+</span> <span class="mi">10</span><span class="p">)</span>
    <span class="n">y_var1</span> <span class="o">=</span> <span class="n">np</span><span class="o">.</span><span class="n">random</span><span class="o">.</span><span class="n">randint</span><span class="p">(</span><span class="mi">1</span><span class="p">,</span> <span class="mi">5</span><span class="p">,</span> <span class="mi">10</span><span class="p">)</span>
    <span class="n">y_var2</span> <span class="o">=</span> <span class="n">np</span><span class="o">.</span><span class="n">random</span><span class="o">.</span><span class="n">randint</span><span class="p">(</span><span class="mi">5</span><span class="p">,</span> <span class="mi">8</span><span class="p">,</span> <span class="mi">10</span><span class="p">)</span>
    <span class="n">plt</span><span class="o">.</span><span class="n">plot</span><span class="p">(</span><span class="n">x</span><span class="p">,</span> <span class="n">y_var1</span><span class="p">,</span> <span class="n">color</span> <span class="o">=</span> <span class="s1">'k'</span><span class="p">,</span> <span class="n">label</span> <span class="o">=</span> <span class="s1">'variable1'</span> <span class="k">if</span> <span class="n">i</span> <span class="o">==</span> <span class="mi"></span> <span class="k">else</span> <span class="s2">"_esto_no_se_pintará"</span><span class="p">)</span>
    <span class="n">plt</span><span class="o">.</span><span class="n">plot</span><span class="p">(</span><span class="n">x</span><span class="p">,</span> <span class="n">y_var2</span><span class="p">,</span> <span class="n">color</span> <span class="o">=</span> <span class="s1">'g'</span><span class="p">,</span> <span class="n">label</span> <span class="o">=</span> <span class="s1">'variable2'</span> <span class="k">if</span> <span class="n">i</span> <span class="o">==</span> <span class="mi"></span> <span class="k">else</span> <span class="s2">"_esto_tampoco"</span><span class="p">)</span>
    <span class="n">plt</span><span class="o">.</span><span class="n">legend</span><span class="p">()</span>
    <span class="n">plt</span><span class="o">.</span><span class="n">ylim</span><span class="p">(</span><span class="mi"></span><span class="p">,</span> <span class="mi">9</span><span class="p">)</span>
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
          <img src="http://new.pybonacci.org/images/2016/06/wpid-Microentradas_Evitar_ciertas_etiquetas_en_la_leyenda_en_Matplotlib-ipynb2.png" alt="" />
        </div>
      </div>
    </div>
  </div>
</div>

<div>
  Espero que a alguien le resulte útil.
</div>