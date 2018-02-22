---
title: ¿Cómo funciona el método append de una lista en CPython?
date: 2015-11-12T23:01:56+00:00
author: Kiko Correoso
slug: como-funciona-el-metodo-append-de-una-lista-en-cpython
tags: append, CPython, implementación, lista

<div>
  <div>
  </div>
  
  <div>
    <div>
      <p>
        Vamos a empezar con más preguntas que respuestas.
      </p>
      
      <p>
        Como sabéis, las listas de Python son <em>arrays</em> dinámicos. Por otro lado, las tuplas son <em>arrays</em> estáticos.
      </p>
      
      <p>
        <strong>¿Qué implica que las listas sean <em>arrays</em> dinámicos?</strong>
      </p>
      
      <p>
        Al ser un array dinámico podemos modificar sus elementos así como extender el array (lista).
      </p>
      
      <p>
        <strong>¿Cómo funciona lo de extender el <em>array</em> (lista)?</strong>
      </p>
      
      <p>
        Cada vez que usamos el método <code>append</code> de las listas se crea una copia de la lista original y se añade un elemento a esa copia para luego borrar el array original.
      </p>
      
      <p>
        <strong>¿Es esto último cierto?</strong>
      </p>
      
      <p>
        Más o menos.
      </p>
      
      <p>
        Todos estaréis conmigo que si cada vez que añadimos un nuevo elemento tenemos que crear una copia y luego eliminar el <em>array</em> original podríamos crear cierto coste/gasto de recursos (en memoria, principalmente, creando copias).
      </p>
      
      <p>
        Veamos un poco de código:
      </p>
    </div>
  </div>
</div>

<div>
  <div>
    <div>
      <div>
        <div class=" highlight hl-ipython3">
          <pre><span class="kn">import</span> <span class="nn">sys</span>

<span class="n">lista</span> <span class="o">=</span> <span class="p">[]</span>
<span class="k">for</span> <span class="n">i</span> <span class="ow">in</span> <span class="nb">range</span><span class="p">(</span><span class="mi">100</span><span class="p">):</span>
    <span class="n">lista</span><span class="o">.</span><span class="n">append</span><span class="p">(</span><span class="n">i</span><span class="p">)</span>
    <span class="n">txt</span> <span class="o">=</span> <span class="s">'número de elementos = {0:&gt;3} , tamaño de la lista = {1:&gt;4}'</span>
    <span class="nb">print</span><span class="p">(</span><span class="n">txt</span><span class="o">.</span><span class="n">format</span><span class="p">(</span><span class="n">i</span> <span class="o">+</span> <span class="mi">1</span><span class="p">,</span> <span class="n">sys</span><span class="o">.</span><span class="n">getsizeof</span><span class="p">(</span><span class="n">lista</span><span class="p">)))</span>
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
          <pre>número de elementos =   1 , tamaño de la lista =   96
número de elementos =   2 , tamaño de la lista =   96
número de elementos =   3 , tamaño de la lista =   96
número de elementos =   4 , tamaño de la lista =   96
número de elementos =   5 , tamaño de la lista =  128
número de elementos =   6 , tamaño de la lista =  128
número de elementos =   7 , tamaño de la lista =  128
número de elementos =   8 , tamaño de la lista =  128
número de elementos =   9 , tamaño de la lista =  192
número de elementos =  10 , tamaño de la lista =  192
número de elementos =  11 , tamaño de la lista =  192
número de elementos =  12 , tamaño de la lista =  192
número de elementos =  13 , tamaño de la lista =  192
número de elementos =  14 , tamaño de la lista =  192
número de elementos =  15 , tamaño de la lista =  192
número de elementos =  16 , tamaño de la lista =  192
número de elementos =  17 , tamaño de la lista =  264
número de elementos =  18 , tamaño de la lista =  264
número de elementos =  19 , tamaño de la lista =  264
número de elementos =  20 , tamaño de la lista =  264
número de elementos =  21 , tamaño de la lista =  264
número de elementos =  22 , tamaño de la lista =  264
número de elementos =  23 , tamaño de la lista =  264
número de elementos =  24 , tamaño de la lista =  264
número de elementos =  25 , tamaño de la lista =  264
número de elementos =  26 , tamaño de la lista =  344
número de elementos =  27 , tamaño de la lista =  344
número de elementos =  28 , tamaño de la lista =  344
número de elementos =  29 , tamaño de la lista =  344
número de elementos =  30 , tamaño de la lista =  344
número de elementos =  31 , tamaño de la lista =  344
número de elementos =  32 , tamaño de la lista =  344
número de elementos =  33 , tamaño de la lista =  344
número de elementos =  34 , tamaño de la lista =  344
número de elementos =  35 , tamaño de la lista =  344
número de elementos =  36 , tamaño de la lista =  432
número de elementos =  37 , tamaño de la lista =  432
número de elementos =  38 , tamaño de la lista =  432
número de elementos =  39 , tamaño de la lista =  432
número de elementos =  40 , tamaño de la lista =  432
número de elementos =  41 , tamaño de la lista =  432
número de elementos =  42 , tamaño de la lista =  432
número de elementos =  43 , tamaño de la lista =  432
número de elementos =  44 , tamaño de la lista =  432
número de elementos =  45 , tamaño de la lista =  432
número de elementos =  46 , tamaño de la lista =  432
número de elementos =  47 , tamaño de la lista =  528
número de elementos =  48 , tamaño de la lista =  528
número de elementos =  49 , tamaño de la lista =  528
número de elementos =  50 , tamaño de la lista =  528
número de elementos =  51 , tamaño de la lista =  528
número de elementos =  52 , tamaño de la lista =  528
número de elementos =  53 , tamaño de la lista =  528
número de elementos =  54 , tamaño de la lista =  528
número de elementos =  55 , tamaño de la lista =  528
número de elementos =  56 , tamaño de la lista =  528
número de elementos =  57 , tamaño de la lista =  528
número de elementos =  58 , tamaño de la lista =  528
número de elementos =  59 , tamaño de la lista =  640
número de elementos =  60 , tamaño de la lista =  640
número de elementos =  61 , tamaño de la lista =  640
número de elementos =  62 , tamaño de la lista =  640
número de elementos =  63 , tamaño de la lista =  640
número de elementos =  64 , tamaño de la lista =  640
número de elementos =  65 , tamaño de la lista =  640
número de elementos =  66 , tamaño de la lista =  640
número de elementos =  67 , tamaño de la lista =  640
número de elementos =  68 , tamaño de la lista =  640
número de elementos =  69 , tamaño de la lista =  640
número de elementos =  70 , tamaño de la lista =  640
número de elementos =  71 , tamaño de la lista =  640
número de elementos =  72 , tamaño de la lista =  640
número de elementos =  73 , tamaño de la lista =  768
número de elementos =  74 , tamaño de la lista =  768
número de elementos =  75 , tamaño de la lista =  768
número de elementos =  76 , tamaño de la lista =  768
número de elementos =  77 , tamaño de la lista =  768
número de elementos =  78 , tamaño de la lista =  768
número de elementos =  79 , tamaño de la lista =  768
número de elementos =  80 , tamaño de la lista =  768
número de elementos =  81 , tamaño de la lista =  768
número de elementos =  82 , tamaño de la lista =  768
número de elementos =  83 , tamaño de la lista =  768
número de elementos =  84 , tamaño de la lista =  768
número de elementos =  85 , tamaño de la lista =  768
número de elementos =  86 , tamaño de la lista =  768
número de elementos =  87 , tamaño de la lista =  768
número de elementos =  88 , tamaño de la lista =  768
número de elementos =  89 , tamaño de la lista =  912
número de elementos =  90 , tamaño de la lista =  912
número de elementos =  91 , tamaño de la lista =  912
número de elementos =  92 , tamaño de la lista =  912
número de elementos =  93 , tamaño de la lista =  912
número de elementos =  94 , tamaño de la lista =  912
número de elementos =  95 , tamaño de la lista =  912
número de elementos =  96 , tamaño de la lista =  912
número de elementos =  97 , tamaño de la lista =  912
número de elementos =  98 , tamaño de la lista =  912
número de elementos =  99 , tamaño de la lista =  912
número de elementos = 100 , tamaño de la lista =  912
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
        En el anterior código hemos creado una lista vacía y le hemos ido añadiendo elementos y hemos obtenido el tamaño de la lista usando la función <code>getsizeof</code> que nos <a href="https://docs.python.org/3/library/sys.html?highlight=sys%20getsizeof#sys.getsizeof">indica el tamaño del objeto en <em>bytes</em></a>. Luego hemos mostrado en pantalla el número de elementos que tiene la lista y el tamaño que ocupa.
      </p>
      
      <p>
        <strong>Pero, ¿qué ocurre?, ¿por qué aumentando el número de elementos, a veces, no aumenta el tamaño del objeto?, ¿por qué luego cambia?, ¿por qué a medida que hay más elementos en la lista tarda más en cambiar el tamaño de la misma?</strong>
      </p>
      
      <p>
        Veamos qué dice el código original de las listas en el repo de Python localizado en <a href="https://hg.python.org/releasing/3.5/file/tip/Objects/listobject.c#l42">Objects/listobject.c</a>.
      </p>
      
      <p>
        A partir de la línea 42 del código C podemos leer:
      </p>
      
      <pre><code>/* This over-allocates proportional to the list size, making room
 * for additional growth.  The over-allocation is mild, but is
 * enough to give linear-time amortized behavior over a long
 * sequence of appends() in the presence of a poorly-performing
 * system realloc().
 * The growth pattern is:  0, 4, 8, 16, 25, 35, 46, 58, 72, 88, ...
 */
new_allocated = (newsize &gt;&gt; 3) + (newsize &lt; 9 ? 3 : 6);

</code></pre>
      
      <p>
        La última línea traducida a Python sería algo así:
      </p>
      
      <pre><code>new_allocated = (newsize &gt;&gt; 3) + (3 if newsize &lt; 9 else 6)

</code></pre>
      
      <p>
        En el primer paréntesis tenemos el <a href="https://wiki.python.org/moin/BitwiseOperators">operador <em>bitwise right shift</em></a>, similar a la versión en C (no hay que olvidar que CPython está escrito en C) mientras que en el segundo paréntesis tenemos el operador ternario (sin duda, un poco más legible que la versión en C).
      </p>
      
      <p>
        <strong>¿Qué está pasando aquí?</strong>
      </p>
      
      <p>
        Los buenos de los <em>core developers</em> de CPython han pensado que si usas un <em>array</em> dinámico será porque quieres hacer 'perrerías' con él, como ampliarlo. Y si lo amplías una vez es probable que lo amplíes varias veces. Es por ello que, normalmente, se usa un un tamaño un poco mayor, basado en el tamaño y siquiendo la regla mostrada más arriba, para el <em>array</em> (lista) y, de esta forma, podemos ampliarlo sin necesidad de crear tantas copias.
      </p>
      
      <p>
        Veamos esto gráficamente:
      </p>
    </div>
  </div>
</div>

<div>
  <div>
  </div>
  
  <div>
    <div>
      <p>
        Importamos matplotlib para poder crear los gráficos.
      </p>
    </div>
  </div>
</div>

<div>
  <div>
    <div>
      <div>
        <div class=" highlight hl-ipython3">
          <pre><span class="kn">import</span> <span class="nn">matplotlib.pyplot</span> <span class="k">as</span> <span class="nn">plt</span>
<span class="n">plt</span><span class="o">.</span><span class="n">style</span><span class="o">.</span><span class="n">use</span><span class="p">(</span><span class="s">'ggplot'</span><span class="p">)</span>
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
      <p>
        Creamos nuestra <code>lista</code> y otra lista que almacenará los tamaños en bytes, <code>sizes</code>.
      </p>
    </div>
  </div>
</div>

<div>
  <div>
    <div>
      <div>
        <div class=" highlight hl-ipython3">
          <pre><span class="n">lista</span> <span class="o">=</span> <span class="nb">list</span><span class="p">([</span><span class="mi">1</span><span class="p">])</span>
<span class="n">sizes</span> <span class="o">=</span> <span class="p">[</span><span class="n">sys</span><span class="o">.</span><span class="n">getsizeof</span><span class="p">(</span><span class="n">lista</span><span class="p">)]</span>

<span class="k">for</span> <span class="n">i</span> <span class="ow">in</span> <span class="nb">range</span><span class="p">(</span><span class="mi">2</span><span class="p">,</span> <span class="mi">100000</span><span class="p">):</span>
    <span class="n">lista</span><span class="o">.</span><span class="n">append</span><span class="p">(</span><span class="n">i</span><span class="p">)</span>
    <span class="n">sizes</span><span class="o">.</span><span class="n">append</span><span class="p">(</span><span class="n">sys</span><span class="o">.</span><span class="n">getsizeof</span><span class="p">(</span><span class="n">lista</span><span class="p">))</span>
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
        Y ahora dibujamos los tamaños en función del número de elementos dentro de la lista:
      </p>
    </div>
  </div>
</div>

<div>
  <div>
    <div>
      <div>
        <div class=" highlight hl-ipython3">
          <pre><span class="n">plt</span><span class="o">.</span><span class="n">figure</span><span class="p">(</span><span class="n">figsize</span> <span class="o">=</span> <span class="p">(</span><span class="mi">10</span><span class="p">,</span><span class="mi">10</span><span class="p">))</span>
<span class="n">plt</span><span class="o">.</span><span class="n">plot</span><span class="p">(</span><span class="n">lista</span><span class="p">,</span> <span class="n">sizes</span><span class="p">)</span>
<span class="n">plt</span><span class="o">.</span><span class="n">xlabel</span><span class="p">(</span><span class="s">'Número de elementos en la lista'</span><span class="p">)</span>
<span class="n">plt</span><span class="o">.</span><span class="n">ylabel</span><span class="p">(</span><span class="s">'Tamaño en bytes para la lista de tamaño $N$'</span><span class="p">)</span>
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
          <pre>&lt;matplotlib.text.Text at 0x7f0655169c88&gt;</pre>
        </div>
      </div>
      
      <div>
        <div>
        </div>
        
        <div>
          <img src="http://new.pybonacci.org/images/2015/11/wpid-¿Cómo_funciona_el_método_append_de_una_lista_en_CPython1.png" alt="" />
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
        Vemos como los "escalones" en el tamaño de la lista con <em>N</em> elementos va aumentando y el escalón cada vez es más largo a medida que aumenta el tamaño de la <code>lista</code>.
      </p>
    </div>
  </div>
</div>

<div>
  <div>
  </div>
  
  <div>
    <div>
      <p>
        Veamos como es el valor del tamaño dividido por el número de elementos de la lista a medida que va aumentando el mismo (los ejes de la gráfica tienen escala logarítmica):
      </p>
    </div>
  </div>
</div>

<div>
  <div>
    <div>
      <div>
        <div class=" highlight hl-ipython3">
          <pre><span class="n">increment</span> <span class="o">=</span> <span class="p">[</span><span class="n">s</span><span class="o">/</span><span class="n">l</span> <span class="k">for</span> <span class="n">s</span><span class="p">,</span> <span class="n">l</span> <span class="ow">in</span> <span class="nb">zip</span><span class="p">(</span><span class="n">sizes</span><span class="p">,</span> <span class="n">lista</span><span class="p">)]</span>

<span class="n">plt</span><span class="o">.</span><span class="n">figure</span><span class="p">(</span><span class="n">figsize</span> <span class="o">=</span> <span class="p">(</span><span class="mi">10</span><span class="p">,</span><span class="mi">10</span><span class="p">))</span>
<span class="n">plt</span><span class="o">.</span><span class="n">yscale</span><span class="p">(</span><span class="s">'log'</span><span class="p">)</span>
<span class="n">plt</span><span class="o">.</span><span class="n">xscale</span><span class="p">(</span><span class="s">'log'</span><span class="p">)</span>
<span class="n">plt</span><span class="o">.</span><span class="n">ylim</span><span class="p">(</span><span class="mi">7</span><span class="p">,</span> <span class="nb">max</span><span class="p">(</span><span class="n">increment</span><span class="p">))</span>
<span class="n">plt</span><span class="o">.</span><span class="n">plot</span><span class="p">(</span><span class="n">lista</span><span class="p">,</span> <span class="n">increment</span><span class="p">)</span>
<span class="n">plt</span><span class="o">.</span><span class="n">xlabel</span><span class="p">(</span><span class="s">'Número de elementos en la lista'</span><span class="p">)</span>
<span class="n">plt</span><span class="o">.</span><span class="n">ylabel</span><span class="p">(</span><span class="s">'Bytes por número de elementos'</span><span class="p">)</span>
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
          <pre>&lt;matplotlib.text.Text at 0x7f06552ada20&gt;</pre>
        </div>
      </div>
      
      <div>
        <div>
        </div>
        
        <div>
          <img src="http://new.pybonacci.org/images/2015/11/wpid-¿Cómo_funciona_el_método_append_de_una_lista_en_CPython2.png" alt="" />
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
        Curioso, ¿no?
      </p>
    </div>
  </div>
</div>

<div>
  <div>
  </div>
  
  <div>
    <div>
      <p>
        Espero que hayáis aprendido tanto como he aprendido yo elaborando esta entrada.
      </p>
    </div>
  </div>
</div>