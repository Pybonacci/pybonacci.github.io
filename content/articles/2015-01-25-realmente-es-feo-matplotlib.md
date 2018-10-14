---
title: ¿Realmente es feo matplotlib?
date: 2015-01-25T20:40:27+00:00
author: Kiko Correoso
slug: realmente-es-feo-matplotlib
tags: estilos, matplotlib.pyplot, styles

<div class="cell border-box-sizing text_cell rendered">
  <div class="inner_cell">
    <div class="text_cell_render border-box-sizing rendered_html">
      En los últimos tiempos he estado leyendo en múltiples sitios que mmatplotlib es feo, que se ve viejuno, que la librería <em>[ponga usted aquí la librería chachiguay que desee]</em> es 'más mejor', que es una biblioteca muy pesada,..., pero nunca he leído una argumentación para refutar esas quejas.</p>
    </div>
  </div>
</div>

<div class="cell border-box-sizing text_cell rendered">
  <div class="inner_cell">
    <div class="text_cell_render border-box-sizing rendered_html">
      Hoy me voy a centrar en la primera queja que he indicado más arriba.</p>
    </div>
  </div>
</div>

<div class="cell border-box-sizing text_cell rendered">
  <div class="prompt input_prompt">
  </div>
  
  <div class="inner_cell">
    <div class="text_cell_render border-box-sizing rendered_html">
      <h1 id="&#191;Es-matplotlib-feo?">
        &#191;Es matplotlib feo?<a class="anchor-link" href="#&#191;Es-matplotlib-feo?">&#182;</a>
      </h1>
    </div>
  </div>
</div>

<div class="cell border-box-sizing text_cell rendered">
  <div class="inner_cell">
    <div class="text_cell_render border-box-sizing rendered_html">
      Cuando se inició el desarrollo de matplotlib el entorno de trabajo era muy diferente al actual. Se hacían gráficas estáticas 2D para ser publicadas en revistas o en la web de hace 10 o más años (ha cambiado un poco el panorama desde entonces). Se inició para ser una alternativa libre a Matlab y es por ello que su API y apariencia es muy parecida a la que ofrece Matlab. De esta forma matplotlib hace gráficos que, de base, son simples y pensados para ser publicados en cualquier sitio sin necesidad de mucha modificación.<br /> A pesar de ofrecer gráficos aceptables de partida (en mi modesta opinión, por supuesto), desde tiempos inmemoriales se puede acceder a la configuración de base y modificarla para el gusto de cada cual. En la versión más antigua que figura en github (0.91.3) podéis encontrar que <a href="https://github.com/matplotlib/matplotlib/blob/v0.91.2/lib/matplotlib/__init__.py#L42"><code>rcParams</code> ya está por ahí</a> (fichero modificado por última vez en 2007). El que hubiera querido <a href="http://matplotlib.org/users/customizing.html">modificar algo de la configuración básica que trae matplotlib lo podría haber hecho sin mucho esfuerzo</a> y hubiera tardado menos que el perdido en escribir una queja por alguna lista de correo, entrada en algún blog, comentario en reddit,...(*)<br /> (*) <em>Ahora con twitter puede que sea más rápido lanzar la queja que modificar eso que tanto te molesta pero seguirá sin haber argumentación, gracias twitter!!</em></p>
    </div>
  </div>
</div>

<div class="cell border-box-sizing text_cell rendered">
  <div class="inner_cell">
    <div class="text_cell_render border-box-sizing rendered_html">
      <h2 id="&#191;Modificar-matplotlib-a--mi-gusto?">
        &#191;Modificar matplotlib a mi gusto?<a class="anchor-link" href="#&#191;Modificar-matplotlib-a--mi-gusto?">&#182;</a>
      </h2>
    </div>
  </div>
</div>

<div class="cell border-box-sizing text_cell rendered">
  <div class="inner_cell">
    <div class="text_cell_render border-box-sizing rendered_html">
      Siempre ha sido relativamente sencillo, de hecho, en su momento desde Pybonacci creamos un repositorio con algo de código que te <a href="http://nbviewer.ipython.org/github/Pybonacci/mpl_styles/blob/master/mpl_styles-examples_of_use.ipynb">ofrecía una serie de decoradores para conseguir nuevos estilos de forma sencilla</a>.</p>
    </div>
  </div>
</div>

<div class="cell border-box-sizing text_cell rendered">
  <div class="inner_cell">
    <div class="text_cell_render border-box-sizing rendered_html">
      Pero desde la versión 1.4 tenemos disponible el <a href="http://matplotlib.org/users/whats_new.html#style-package-added">paquete <code>styles</code></a> que permite cambiar de estilos fácilmente y que trae algunos estilos por defecto. Veamos un poco como funciona todo esto:</p>
    </div>
  </div>
</div>

<div class="cell border-box-sizing text_cell rendered">
  <div class="inner_cell">
    <div class="text_cell_render border-box-sizing rendered_html">
      Primero de todo hacemos todo el previo de imports y mostrar versiones y demás para que el que quiera pueda reproducir los ejemplos sin problemas.</p>
    </div>
  </div>
</div>

<div class="cell border-box-sizing code_cell rendered">
  <div class="input">
    <div class="inner_cell">
      <div class="input_area">
        <div class=" highlight hl-ipython">
          <pre><span class="c">#%install_ext http://raw.github.com/jrjohansson/version_information/master/version_information.py</span>
<span class="o">%</span><span class="k">load_ext</span> <span class="n">version_information</span>
</pre>
        </div>
      </div>
    </div>
  </div>
</div>

<div class="cell border-box-sizing code_cell rendered">
  <div class="input">
    <div class="inner_cell">
      <div class="input_area">
        <div class=" highlight hl-ipython">
          <pre><span class="o">%</span><span class="k">version_information</span> <span class="n">matplotlib</span><span class="p">,</span> <span class="n">numpy</span>
</pre>
        </div>
      </div>
    </div>
  </div>
  
  <div class="output_wrapper">
    <div class="output">
      <div class="output_area">
        <div class="prompt">
        </div>
      </div>
      
      <div class="output_area">
        <div class="output_html rendered_html output_subarea output_pyout">
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
                3.4.0 64bit [GCC 4.8.2]
              </td>
            </tr>
            
            <tr>
              <td>
                IPython
              </td>
              
              <td>
                3.0.0-dev
              </td>
            </tr>
            
            <tr>
              <td>
                OS
              </td>
              
              <td>
                Linux 3.13.0 24 generic x86_64 with LinuxMint 17 qiana
              </td>
            </tr>
            
            <tr>
              <td>
                matplotlib
              </td>
              
              <td>
                1.4.2
              </td>
            </tr>
            
            <tr>
              <td>
                numpy
              </td>
              
              <td>
                1.9.1
              </td>
            </tr>
            
            <tr>
              <td colspan='2'>
                Sun Jan 25 19:51:49 2015 CET
              </td>
            </tr>
          </table>
        </div>
      </div>
    </div>
  </div>
</div>

<div class="cell border-box-sizing code_cell rendered">
  <div class="input">
    <div class="inner_cell">
      <div class="input_area">
        <div class=" highlight hl-ipython">
          <pre><span class="o">%</span><span class="k">matplotlib</span> <span class="n">inline</span>

<span class="kn">import</span> <span class="nn">matplotlib.pyplot</span> <span class="kn">as</span> <span class="nn">plt</span>
<span class="kn">import</span> <span class="nn">numpy</span> <span class="kn">as</span> <span class="nn">np</span>
</pre>
        </div>
      </div>
    </div>
  </div>
</div>

<div class="cell border-box-sizing text_cell rendered">
  <div class="inner_cell">
    <div class="text_cell_render border-box-sizing rendered_html">
      Un gráfico normal por defecto en matplotlib (de esos que son tan feos) en el notebook de IPython será de la siguiente forma:</p>
    </div>
  </div>
</div>

<div class="cell border-box-sizing code_cell rendered">
  <div class="input">
    <div class="inner_cell">
      <div class="input_area">
        <div class=" highlight hl-ipython">
          <pre><span class="n">fig</span><span class="p">,</span> <span class="n">ax</span> <span class="o">=</span> <span class="n">plt</span><span class="o">.</span><span class="n">subplots</span><span class="p">(</span><span class="n">figsize</span><span class="o">=</span><span class="p">(</span><span class="mi">8</span><span class="p">,</span><span class="mi">4</span><span class="p">))</span>
<span class="n">ax</span><span class="o">.</span><span class="n">plot</span><span class="p">(</span><span class="n">np</span><span class="o">.</span><span class="n">random</span><span class="o">.</span><span class="n">randn</span><span class="p">(</span><span class="mi">25</span><span class="p">),</span> <span class="n">label</span> <span class="o">=</span> <span class="s">&#039;random&#039;</span><span class="p">)</span>
<span class="n">ax</span><span class="o">.</span><span class="n">legend</span><span class="p">()</span>
</pre>
        </div>
      </div>
    </div>
  </div>
  
  <div class="output_wrapper">
    <div class="output">
      <div class="output_area">
      </div>
      
      <div class="output_area">
        <div class="prompt">
        </div>
        
        <div class="output_png output_subarea ">
          <img src="https://pybonacci.org/images/2015/01/wpid-¿Realmente_es_feo_matplotlib1.png" />
        </div>
      </div>
    </div>
  </div>
</div>

<div class="cell border-box-sizing text_cell rendered">
  <div class="inner_cell">
    <div class="text_cell_render border-box-sizing rendered_html">
      Usando el paquete <code>styles</code> modificar la apariencia a uno de los estilos que trae por defecto el paquete sería algo como lo siguiente:</p>
    </div>
  </div>
</div>

<div class="cell border-box-sizing code_cell rendered">
  <div class="input">
    <div class="inner_cell">
      <div class="input_area">
        <div class=" highlight hl-ipython">
          <pre><span class="k">print</span><span class="p">(</span><span class="s">&#039;Estilos disponibles: &#039;</span><span class="p">,</span> <span class="n">plt</span><span class="o">.</span><span class="n">style</span><span class="o">.</span><span class="n">available</span><span class="p">)</span>
<span class="n">estilo</span> <span class="o">=</span> <span class="n">np</span><span class="o">.</span><span class="n">random</span><span class="o">.</span><span class="n">choice</span><span class="p">(</span><span class="n">plt</span><span class="o">.</span><span class="n">style</span><span class="o">.</span><span class="n">available</span><span class="p">)</span>
<span class="k">print</span><span class="p">(</span><span class="s">&#039;Vamos a usar el estilo &#039;</span><span class="p">,</span> <span class="n">estilo</span><span class="p">)</span>
<span class="n">plt</span><span class="o">.</span><span class="n">style</span><span class="o">.</span><span class="n">use</span><span class="p">(</span><span class="n">estilo</span><span class="p">)</span>

<span class="c"># la misma gráfica que antes</span>
<span class="n">fig</span><span class="p">,</span> <span class="n">ax</span> <span class="o">=</span> <span class="n">plt</span><span class="o">.</span><span class="n">subplots</span><span class="p">(</span><span class="n">figsize</span><span class="o">=</span><span class="p">(</span><span class="mi">8</span><span class="p">,</span><span class="mi">4</span><span class="p">))</span>
<span class="n">ax</span><span class="o">.</span><span class="n">plot</span><span class="p">(</span><span class="n">np</span><span class="o">.</span><span class="n">random</span><span class="o">.</span><span class="n">randn</span><span class="p">(</span><span class="mi">25</span><span class="p">),</span> <span class="n">label</span> <span class="o">=</span> <span class="s">&#039;random&#039;</span><span class="p">)</span>
<span class="n">ax</span><span class="o">.</span><span class="n">legend</span><span class="p">()</span>
</pre>
        </div>
      </div>
    </div>
  </div>
  
  <div class="output_wrapper">
    <div class="output">
      <div class="output_area">
        <div class="prompt">
        </div>
        
        <div class="output_subarea output_stream output_stdout output_text">
          <pre>Estilos disponibles:  [';fivethirtyeight';, ';ggplot';, ';grayscale';, ';dark_background';, ';bmh';]
Vamos a usar el estilo  ggplot
</pre>
        </div>
      </div>
      
      <div class="output_area">
      </div>
      
      <div class="output_area">
        <div class="prompt">
        </div>
        
        <div class="output_png output_subarea ">
          <img src="https://pybonacci.org/images/2015/01/wpid-¿Realmente_es_feo_matplotlib2.png" />
        </div>
      </div>
    </div>
  </div>
</div>

<div class="cell border-box-sizing text_cell rendered">
  <div class="inner_cell">
    <div class="text_cell_render border-box-sizing rendered_html">
      Como habéis visto en la salida anterior disponéis de varios estilos por defecto, <code>['ggplot', 'bmh', 'grayscale', 'dark_background', 'fivethirtyeight']</code>. Probadlos todos si queréis verlos en vivo o <a href="http://nbviewer.ipython.org/github/jakevdp/PyData2014/blob/master/notebooks/06_mpl_Stylesheets.ipynb">ved este notebook</a>.<br /> Si os gustan los valores por defecto podéis volver a ellos usando <code>plt.rcdefaults()</code>.</p>
    </div>
  </div>
</div>

<div class="cell border-box-sizing text_cell rendered">
  <div class="inner_cell">
    <div class="text_cell_render border-box-sizing rendered_html">
      <h2 id="No-me-gusta-ninguno-de-los-estilos-que-vienen-por-defecto">
        No me gusta ninguno de los estilos que vienen por defecto<a class="anchor-link" href="#No-me-gusta-ninguno-de-los-estilos-que-vienen-por-defecto">&#182;</a>
      </h2>
    </div>
  </div>
</div>

<div class="cell border-box-sizing text_cell rendered">
  <div class="inner_cell">
    <div class="text_cell_render border-box-sizing rendered_html">
      "Siemprrre negatifffos, nunca positifffos", pero que no cunda el desánimo. Crear tu propio estilo es sencillo. Vamos a ver como podemos crear una hoja de estilos que se adecúe a nuestros gustos.</p>
    </div>
  </div>
</div>

<div class="cell border-box-sizing text_cell rendered">
  <div class="inner_cell">
    <div class="text_cell_render border-box-sizing rendered_html">
      Si queremos que nuestro nuevo estilo esté siempre disponible cada vez que usemos matplotlib deberemos incluir la hoja de estilos en la carpeta <strike><code>~/.matplotlib/stylelib/</code></strike> <code>~/.config/matplotlib/stylelib/</code> (la documentación oficial está mal y deberéis usar la que os indico yo, quizá esa carpeta no exista de inicio y la deberéis de crear). Voy a crearla con IPython (lo hago en Linux, no lo he probado en otros sistemas operativos):</p>
    </div>
  </div>
</div>

<div class="cell border-box-sizing code_cell rendered">
  <div class="input">
    <div class="inner_cell">
      <div class="input_area">
        <div class=" highlight hl-ipython">
          <pre><span class="o">%</span><span class="k">mkdir</span> <span class="o">~/.</span><span class="n">config</span> <span class="c"># Seguramente esta ya exista</span>
<span class="o">%</span><span class="k">mkdir</span> <span class="o">~/.</span><span class="n">config</span><span class="o">/</span><span class="n">matplotlib</span>
<span class="o">%</span><span class="k">mkdir</span> <span class="o">~/.</span><span class="n">config</span><span class="o">/</span><span class="n">matplotlib</span><span class="o">/</span><span class="n">stylelib</span>
</pre>
        </div>
      </div>
    </div>
  </div>
  
  <div class="output_wrapper">
    <div class="output">
      <div class="output_area">
        <div class="prompt">
        </div>
      </div>
    </div>
  </div>
</div>

<div class="cell border-box-sizing text_cell rendered">
  <div class="inner_cell">
    <div class="text_cell_render border-box-sizing rendered_html">
      Y ahora vamos a definir un nuevo estilo <strong>pybonacci</strong> como el que <a href="https://github.com/Pybonacci/mpl_styles/blob/master/mpl_styles.py#L117">definimos en el repositorio de <em>mpl_styles</em></a>. Para ello vamos a usar IPython para crear la hoja de estilo que se llamará <code>pybonacci.mplstyle</code> (debe tener la extensión <code>\*.mplstyle</code>):</p>
    </div>
  </div>
</div>

<div class="cell border-box-sizing code_cell rendered">
  <div class="input">
    <div class="inner_cell">
      <div class="input_area">
        <div class=" highlight hl-ipython">
          <pre><span class="o">%%</span><span class="k">writefile</span> <span class="o">~/.</span><span class="n">config</span><span class="o">/</span><span class="n">matplotlib</span><span class="o">/</span><span class="n">stylelib</span><span class="o">/</span><span class="n">pybonacci</span><span class="o">.</span><span class="n">mplstyle</span>
<span class="n">lines</span><span class="o">.</span><span class="n">linewidth</span><span class="p">:</span> <span class="mf">1.0</span>
<span class="n">lines</span><span class="o">.</span><span class="n">color</span><span class="p">:</span> <span class="mi">5390</span><span class="n">C1</span>
<span class="n">lines</span><span class="o">.</span><span class="n">antialiased</span><span class="p">:</span> <span class="bp">True</span>
<span class="n">patch</span><span class="o">.</span><span class="n">linewidth</span><span class="p">:</span> <span class="mf">0.5</span>
<span class="n">patch</span><span class="o">.</span><span class="n">facecolor</span><span class="p">:</span> <span class="n">FFD333</span>
<span class="n">patch</span><span class="o">.</span><span class="n">edgecolor</span><span class="p">:</span> <span class="n">FFE771</span>
<span class="n">patch</span><span class="o">.</span><span class="n">antialiased</span><span class="p">:</span> <span class="bp">True</span>
<span class="n">font</span><span class="o">.</span><span class="n">family</span><span class="p">:</span> <span class="n">Arial</span>
<span class="n">font</span><span class="o">.</span><span class="n">size</span><span class="p">:</span> <span class="mf">10.0</span>
<span class="n">font</span><span class="o">.</span><span class="n">monospace</span><span class="p">:</span> <span class="n">DejaVu</span> <span class="n">Sans</span> <span class="n">Mono</span><span class="p">,</span> <span class="n">Andale</span> <span class="n">Mono</span><span class="p">,</span> <span class="n">Nimbus</span> <span class="n">Mono</span> <span class="n">L</span><span class="p">,</span> <span class="n">Courier</span> <span class="n">New</span><span class="p">,</span> <span class="n">Courier</span><span class="p">,</span> <span class="n">Fixed</span><span class="p">,</span> <span class="n">Terminal</span><span class="p">,</span> <span class="n">monospace</span>
<span class="n">axes</span><span class="o">.</span><span class="n">facecolor</span><span class="p">:</span> <span class="n">eeeeee</span>
<span class="n">axes</span><span class="o">.</span><span class="n">edgecolor</span><span class="p">:</span> <span class="n">bcbcbc</span>
<span class="n">axes</span><span class="o">.</span><span class="n">linewidth</span><span class="p">:</span> <span class="mf">1.0</span>
<span class="n">axes</span><span class="o">.</span><span class="n">grid</span><span class="p">:</span> <span class="bp">True</span>
<span class="n">axes</span><span class="o">.</span><span class="n">titlesize</span><span class="p">:</span> <span class="n">x</span><span class="o">-</span><span class="n">large</span>
<span class="n">axes</span><span class="o">.</span><span class="n">labelsize</span><span class="p">:</span> <span class="n">large</span>
<span class="n">axes</span><span class="o">.</span><span class="n">labelcolor</span><span class="p">:</span> <span class="mi">555555</span>
<span class="n">axes</span><span class="o">.</span><span class="n">axisbelow</span><span class="p">:</span> <span class="bp">True</span>
<span class="n">axes</span><span class="o">.</span><span class="n">color_cycle</span><span class="p">:</span> <span class="mi">5390</span><span class="n">C1</span><span class="p">,</span> <span class="n">FFD333</span><span class="p">,</span> <span class="n">FFE771</span><span class="p">,</span> <span class="mi">70</span><span class="n">A4CB</span><span class="p">,</span> <span class="mi">4385</span><span class="n">BB</span><span class="p">,</span> <span class="mi">3</span><span class="n">D79AA</span><span class="p">,</span> <span class="mi">39719</span><span class="n">E</span>
<span class="n">xtick</span><span class="o">.</span><span class="n">major</span><span class="o">.</span><span class="n">size</span><span class="p">:</span> <span class="mf">0.0</span>
<span class="n">xtick</span><span class="o">.</span><span class="n">minor</span><span class="o">.</span><span class="n">size</span><span class="p">:</span> <span class="mf">0.0</span>
<span class="n">xtick</span><span class="o">.</span><span class="n">major</span><span class="o">.</span><span class="n">pad</span><span class="p">:</span> <span class="mf">6.0</span>
<span class="n">xtick</span><span class="o">.</span><span class="n">minor</span><span class="o">.</span><span class="n">pad</span><span class="p">:</span> <span class="mf">6.0</span>
<span class="n">xtick</span><span class="o">.</span><span class="n">color</span><span class="p">:</span> <span class="mi">555555</span>
<span class="n">xtick</span><span class="o">.</span><span class="n">direction</span><span class="p">:</span> <span class="ow">in</span>
<span class="n">ytick</span><span class="o">.</span><span class="n">major</span><span class="o">.</span><span class="n">size</span><span class="p">:</span> <span class="mf">0.0</span>
<span class="n">ytick</span><span class="o">.</span><span class="n">minor</span><span class="o">.</span><span class="n">size</span><span class="p">:</span> <span class="mf">0.0</span>
<span class="n">ytick</span><span class="o">.</span><span class="n">major</span><span class="o">.</span><span class="n">pad</span><span class="p">:</span> <span class="mf">6.0</span>
<span class="n">ytick</span><span class="o">.</span><span class="n">minor</span><span class="o">.</span><span class="n">pad</span><span class="p">:</span> <span class="mf">6.0</span>
<span class="n">ytick</span><span class="o">.</span><span class="n">color</span><span class="p">:</span> <span class="mi">555555</span>
<span class="n">ytick</span><span class="o">.</span><span class="n">direction</span><span class="p">:</span> <span class="ow">in</span>
<span class="n">legend</span><span class="o">.</span><span class="n">fancybox</span><span class="p">:</span> <span class="bp">True</span>
<span class="n">legend</span><span class="o">.</span><span class="n">numpoints</span><span class="p">:</span> <span class="mi">1</span>
<span class="n">figure</span><span class="o">.</span><span class="n">figsize</span><span class="p">:</span> <span class="mi">11</span><span class="p">,</span> <span class="mi">8</span>
<span class="n">figure</span><span class="o">.</span><span class="n">facecolor</span><span class="p">:</span> <span class="mf">1.0</span>
<span class="n">figure</span><span class="o">.</span><span class="n">edgecolor</span><span class="p">:</span> <span class="mf">0.5</span>
<span class="n">figure</span><span class="o">.</span><span class="n">subplot</span><span class="o">.</span><span class="n">hspace</span><span class="p">:</span> <span class="mf">0.5</span>
</pre>
        </div>
      </div>
    </div>
  </div>
  
  <div class="output_wrapper">
    <div class="output">
      <div class="output_area">
        <div class="prompt">
        </div>
        
        <div class="output_subarea output_stream output_stdout output_text">
          <pre>Writing /home/kiko/.config/matplotlib/stylelib/pybonacci.mplstyle
</pre>
        </div>
      </div>
    </div>
  </div>
</div>

<div class="cell border-box-sizing text_cell rendered">
  <div class="inner_cell">
    <div class="text_cell_render border-box-sizing rendered_html">
      Y ahora, supuestamente, deberíamos poder acceder al nuevo estilo creado:</p>
    </div>
  </div>
</div>

<div class="cell border-box-sizing code_cell rendered">
  <div class="input">
    <div class="inner_cell">
      <div class="input_area">
        <div class=" highlight hl-ipython">
          <pre><span class="k">print</span><span class="p">(</span><span class="s">&#039;Estilos disponibles: &#039;</span><span class="p">,</span> <span class="n">plt</span><span class="o">.</span><span class="n">style</span><span class="o">.</span><span class="n">available</span><span class="p">)</span>
</pre>
        </div>
      </div>
    </div>
  </div>
  
  <div class="output_wrapper">
    <div class="output">
      <div class="output_area">
        <div class="prompt">
        </div>
        
        <div class="output_subarea output_stream output_stdout output_text">
          <pre>Estilos disponibles:  [';fivethirtyeight';, ';ggplot';, ';grayscale';, ';dark_background';, ';bmh';]
</pre>
        </div>
      </div>
    </div>
  </div>
</div>

<div class="cell border-box-sizing text_cell rendered">
  <div class="inner_cell">
    <div class="text_cell_render border-box-sizing rendered_html">
      Si veis que no está disponible podéis hacer lo siguiente:</p>
    </div>
  </div>
</div>

<div class="cell border-box-sizing code_cell rendered">
  <div class="input">
    <div class="inner_cell">
      <div class="input_area">
        <div class=" highlight hl-ipython">
          <pre><span class="n">plt</span><span class="o">.</span><span class="n">style</span><span class="o">.</span><span class="n">reload_library</span><span class="p">()</span>
<span class="n">plt</span><span class="o">.</span><span class="n">style</span><span class="o">.</span><span class="n">available</span>
</pre>
        </div>
      </div>
    </div>
  </div>
  
  <div class="output_wrapper">
    <div class="output">
      <div class="output_area">
        <div class="output_text output_subarea output_pyout">
          <pre>[';ggplot';,
 ';grayscale';,
 ';dark_background';,
 ';bmh';,
 ';fivethirtyeight';,
 ';pybonacci';]</pre>
        </div>
      </div>
    </div>
  </div>
</div>

<div class="cell border-box-sizing text_cell rendered">
  <div class="inner_cell">
    <div class="text_cell_render border-box-sizing rendered_html">
      Ahora vamos a recrear el gráfico que <a href="https://github.com/Pybonacci/mpl_styles/blob/master/mpl_styles.py#L117">definimos en el repositorio de <em>mpl_styles</em></a> para el estilo <strong>pybo</strong> que definimos allí:</p>
    </div>
  </div>
</div>

<div class="cell border-box-sizing code_cell rendered">
  <div class="input">
    <div class="inner_cell">
      <div class="input_area">
        <div class=" highlight hl-ipython">
          <pre><span class="n">plt</span><span class="o">.</span><span class="n">style</span><span class="o">.</span><span class="n">use</span><span class="p">(</span><span class="s">&#039;pybonacci&#039;</span><span class="p">)</span>

<span class="n">x1</span> <span class="o">=</span> <span class="nb">range</span><span class="p">(</span><span class="mi">10</span><span class="p">)</span>
<span class="n">x2</span> <span class="o">=</span> <span class="n">np</span><span class="o">.</span><span class="n">random</span><span class="o">.</span><span class="n">rand</span><span class="p">(</span><span class="mi">100</span><span class="p">)</span>
<span class="n">y1</span> <span class="o">=</span> <span class="n">np</span><span class="o">.</span><span class="n">random</span><span class="o">.</span><span class="n">randn</span><span class="p">(</span><span class="mi">10</span><span class="p">)</span>
<span class="n">y2</span> <span class="o">=</span> <span class="n">np</span><span class="o">.</span><span class="n">random</span><span class="o">.</span><span class="n">rand</span><span class="p">(</span><span class="mi">100</span><span class="p">)</span>

<span class="n">plt</span><span class="o">.</span><span class="n">subplot</span><span class="p">(</span><span class="mi">2</span><span class="p">,</span><span class="mi">2</span><span class="p">,</span><span class="mi">1</span><span class="p">)</span>
<span class="n">plt</span><span class="o">.</span><span class="n">plot</span><span class="p">(</span><span class="n">x1</span><span class="p">,</span><span class="n">y1</span><span class="p">)</span>
<span class="n">plt</span><span class="o">.</span><span class="n">plot</span><span class="p">(</span><span class="n">x1</span><span class="p">,</span><span class="n">y1</span><span class="o">-</span><span class="mi">1</span><span class="p">)</span>
<span class="n">plt</span><span class="o">.</span><span class="n">plot</span><span class="p">(</span><span class="n">x1</span><span class="p">,</span><span class="n">y1</span><span class="o">-</span><span class="mi">2</span><span class="p">)</span>
<span class="n">plt</span><span class="o">.</span><span class="n">plot</span><span class="p">(</span><span class="n">x1</span><span class="p">,</span><span class="n">y1</span><span class="o">-</span><span class="mi">3</span><span class="p">)</span>
<span class="n">plt</span><span class="o">.</span><span class="n">plot</span><span class="p">(</span><span class="n">x1</span><span class="p">,</span><span class="n">y1</span><span class="o">-</span><span class="mi">4</span><span class="p">)</span>
<span class="n">plt</span><span class="o">.</span><span class="n">subplot</span><span class="p">(</span><span class="mi">2</span><span class="p">,</span><span class="mi">2</span><span class="p">,</span><span class="mi">2</span><span class="p">)</span>
<span class="n">plt</span><span class="o">.</span><span class="n">scatter</span><span class="p">(</span><span class="n">x2</span><span class="p">,</span> <span class="n">y2</span><span class="p">)</span>
<span class="n">plt</span><span class="o">.</span><span class="n">subplot</span><span class="p">(</span><span class="mi">2</span><span class="p">,</span><span class="mi">2</span><span class="p">,</span><span class="mi">3</span><span class="p">)</span>
<span class="n">plt</span><span class="o">.</span><span class="n">bar</span><span class="p">(</span><span class="n">x1</span><span class="p">,</span> <span class="n">y1</span><span class="p">)</span>
</pre>
        </div>
      </div>
    </div>
  </div>
  
  <div class="output_wrapper">
    <div class="output">
      <div class="output_area">
      </div>
      
      <div class="output_area">
        <div class="prompt">
        </div>
        
        <div class="output_png output_subarea ">
          <img src="https://pybonacci.org/images/2015/01/wpid-¿Realmente_es_feo_matplotlib3.png" />
        </div>
      </div>
    </div>
  </div>
</div>

<div class="cell border-box-sizing text_cell rendered">
  <div class="prompt input_prompt">
  </div>
  
  <div class="inner_cell">
    <div class="text_cell_render border-box-sizing rendered_html">
      <h2 id="Que-he-dicho-que-no-me-gusta-matplotlib">
        Que he dicho que no me gusta matplotlib<a class="anchor-link" href="#Que-he-dicho-que-no-me-gusta-matplotlib">&#182;</a>
      </h2>
    </div>
  </div>
</div>

<div class="cell border-box-sizing text_cell rendered">
  <div class="prompt input_prompt">
  </div>
  
  <div class="inner_cell">
    <div class="text_cell_render border-box-sizing rendered_html">
      Si a pesar de todo lo expuesto aquí sigue sin gustarte matplotlib (estás en tu derecho y si lo argumentas en los comentarios lo podré entender mejor) tienes varias posibilidades disponibles:</p> 
      
      <ul>
        <li>
          <a href="http://bokeh.pydata.org/en/latest/">Bokeh</a>
        </li>
        <li>
          <a href="http://ggplot.yhathq.com/">GGplot</a>
        </li>
        <li>
          Usad alguna librería javascript como Highcharts (<a href="https://pybonacci.org/2014/07/31/tutorial-de-highcharts-usando-ipython-brython-y-brythonmagic/">ved un tutorial aquí</a>), d3js,...
        </li>
        <li>
          <a href="http://code.enthought.com/chaco/">Chaco</a>
        </li>
        <li>
          <a href="http://home.gna.org/veusz/">Veusz</a>
        </li>
        <li>
          <a href="http://pyqwt.sourceforge.net/">PyQwt</a>
        </li>
      </ul>
      
      <p>
        No pongo <a href="http://stanford.edu/~mwaskom/software/seaborn/index.html">Seaborn</a> puesto que se basa en matplotlib.
      </p>
    </div>
  </div>
</div>

<div class="cell border-box-sizing text_cell rendered">
  <div class="prompt input_prompt">
  </div>
  
  <div class="inner_cell">
    <div class="text_cell_render border-box-sizing rendered_html">
      Saludos a todos.<br /> P.D.: Este notebook y la hoja de estilos que acabamos de crear está disponible en el <a href="https://github.com/Pybonacci/notebooks/tree/master/Realmente_es_feo_matplotlib">repo de notebooks de Pybonacci</a>.</p>
    </div>
  </div>
</div>