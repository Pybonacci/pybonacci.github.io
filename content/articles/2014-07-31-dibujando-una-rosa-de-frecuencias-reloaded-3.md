---
title: Dibujando una rosa de frecuencias (reloaded)
date: 2014-07-31T02:28:30+00:00
author: Kiko Correoso
slug: dibujando-una-rosa-de-frecuencias-reloaded-3
tags: gráficos, math, matplotlib, numpy, python, python 3

<div class="cell border-box-sizing text_cell rendered">
  <div class="prompt input_prompt">
  </div>
  
  <div class="inner_cell">
    <div class="text_cell_render border-box-sizing rendered_html">
      <strong>Esta entrada es una actualización a la entrada <a href="https://pybonacci.org/2012/03/24/dibujando-una-rosa-de-frecuencias/">Dibujando una rosa de frecuencias</a> dónde se rehace el código para usar nuevas funcionalidades de matplotlib que simplifica el script.</strong><br /> Imaginaos que estáis de vacaciones en Agosto en la playa y la única preocupación que tenéis es observar las nubes. Como sois un poco frikis y no podéis desconectar de vuestra curiosidad científica decidís apuntar las ocurrencias de la procedencia de las nubes y al final de las vacaciones decidís representar esos datos. La forma más normal de hacerlo sería usando una rosa de frecuencias.<br /> Primero de todo vamos a importar los módulos que nos harán falta:
    </div>
  </div>
</div>

<div class="cell border-box-sizing code_cell rendered">
  <div class="input">
    <div class="prompt input_prompt">
      In&nbsp;[2]:
    </div>
    
    <div class="inner_cell">
      <div class="input_area">
        <div class="highlight">
          <pre><span class="kn">import</span> <span class="nn">sys</span>

<span class="kn">import</span> <span class="nn">numpy</span> <span class="kn">as</span> <span class="nn">np</span>
<span class="kn">import</span> <span class="nn">matplotlib.pyplot</span> <span class="kn">as</span> <span class="nn">plt</span>
<span class="kn">import</span> <span class="nn">matplotlib</span>
<span class="kn">import</span> <span class="nn">math</span>

<span class="o">%</span><span class="k">matplotlib</span> <span class="n">inline</span>

<span class="k">print</span><span class="p">(</span><span class="s">&#039;Versión de Python usada: &#039;</span><span class="p">,</span> <span class="n">sys</span><span class="o">.</span><span class="n">version</span><span class="p">)</span>
<span class="k">print</span><span class="p">(</span><span class="s">&#039;Versión de Numpy usada: &#039;</span><span class="p">,</span> <span class="n">np</span><span class="o">.</span><span class="n">__version__</span><span class="p">)</span>
<span class="k">print</span><span class="p">(</span><span class="s">&#039;Versión de Matplotlib usada: &#039;</span><span class="p">,</span> <span class="n">matplotlib</span><span class="o">.</span><span class="n">__version__</span><span class="p">)</span>
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
          <pre>
Versión de Python usada:  3.4.1 (v3.4.1:c0e311e010fc, May 18 2014, 10:38:22) [MSC v.1600 32 bit (Intel)]
Versión de Numpy usada:  1.8.1
Versión de Matplotlib usada:  1.3.1

</pre>
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
      A continuación creamos nuestra muestra de datos totalmente inventada:
    </div>
  </div>
</div>

<div class="cell border-box-sizing code_cell rendered">
  <div class="input">
    <div class="prompt input_prompt">
      In&nbsp;[3]:
    </div>
    
    <div class="inner_cell">
      <div class="input_area">
        <div class="highlight">
          <pre><span class="c">## Creamos un conjunto de datos</span>
<span class="n">datos</span> <span class="o">=</span> <span class="n">np</span><span class="o">.</span><span class="n">arange</span><span class="p">(</span><span class="mi">10</span><span class="p">,</span><span class="mi">90</span><span class="p">,</span><span class="mi">10</span><span class="p">)</span>
<span class="c">## Los datos los queremos en tanto por ciento</span>
<span class="n">datos</span> <span class="o">=</span> <span class="n">datos</span> <span class="o">*</span> <span class="mf">100.</span> <span class="o">/</span> <span class="n">datos</span><span class="o">.</span><span class="n">sum</span><span class="p">()</span>
<span class="c">## Direcciones en radianes empezando por el N</span>
<span class="c">## A las direcciones les restamos 22.5º para que las barras</span>
<span class="c">## estén centradas exactamente en 0, 45, 90,...</span>
<span class="n">direcciones</span> <span class="o">=</span> <span class="p">(</span><span class="n">np</span><span class="o">.</span><span class="n">arange</span><span class="p">(</span><span class="mi"></span><span class="p">,</span> <span class="mi">360</span><span class="p">,</span> <span class="mi">45</span><span class="p">)</span> <span class="o">-</span> <span class="mf">22.5</span><span class="p">)</span> <span class="o">*</span> <span class="n">math</span><span class="o">.</span><span class="n">pi</span> <span class="o">/</span> <span class="mf">180.</span>
<span class="n">sectores</span> <span class="o">=</span> <span class="p">[</span><span class="s">&#039;N&#039;</span><span class="p">,</span><span class="s">&#039;NE&#039;</span><span class="p">,</span><span class="s">&#039;E&#039;</span><span class="p">,</span><span class="s">&#039;SE&#039;</span><span class="p">,</span><span class="s">&#039;S&#039;</span><span class="p">,</span><span class="s">&#039;SW&#039;</span><span class="p">,</span><span class="s">&#039;W&#039;</span><span class="p">,</span><span class="s">&#039;NW&#039;</span><span class="p">]</span>
</pre>
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
      En el bloque anterior de código, lo único que hemos hecho es crear un conjunto de datos sin sentido y los hemos separado en 8 intervalos que pretenden ser las 8 direcciones de donde provienen las nubes empezando por el Norte y en el sentido de las agujas del reloj. Finalmente los datos los expresamos como frecuencia en tanto por ciento en cada una de las 8 direcciones.<br /> Matplotlib nos permite hacer gráficos polares <s>pero estos gráficos están pensados para gráficos en sentido contrario a las agujas del reloj y empezando a las tres en punto (o al este). Por ello debemos modificar como se verán los datos en el gráfico polar</s>. Para ello definimos el tipo de gráfico, colocamos el nombre de la dirección en cada sector definido (en este caso hemos usado 8 sectores), ponemos un título a nuestro gráfico y hemos acabado.
    </div>
  </div>
</div>

<div class="cell border-box-sizing code_cell rendered">
  <div class="input">
    <div class="prompt input_prompt">
      In&nbsp;[4]:
    </div>
    
    <div class="inner_cell">
      <div class="input_area">
        <div class="highlight">
          <pre><span class="n">fig</span> <span class="o">=</span> <span class="n">plt</span><span class="o">.</span><span class="n">figure</span><span class="p">(</span><span class="n">figsize</span> <span class="o">=</span> <span class="p">(</span><span class="mi">10</span><span class="p">,</span><span class="mi">10</span><span class="p">))</span>
<span class="n">ax</span> <span class="o">=</span> <span class="n">fig</span><span class="o">.</span><span class="n">add_subplot</span><span class="p">(</span><span class="mi">111</span><span class="p">,</span> <span class="n">polar</span><span class="o">=</span><span class="bp">True</span><span class="p">)</span>
<span class="c">## La siguiente línea de código hace que los datos vayan en el </span>
<span class="c">## sentido de las agujas del reloj</span>
<span class="n">ax</span><span class="o">.</span><span class="n">set_theta_direction</span><span class="p">(</span><span class="o">-</span><span class="mi">1</span><span class="p">)</span>
<span class="c">## La siguiente línea de código coloca el &#039;origen&#039; de la rotación</span>
<span class="c">## donde le indiquemos, en este caso em Norte.</span>
<span class="n">ax</span><span class="o">.</span><span class="n">set_theta_zero_location</span><span class="p">(</span><span class="s">&#039;N&#039;</span><span class="p">)</span>
<span class="c">## Título</span>
<span class="n">ax</span><span class="o">.</span><span class="n">set_title</span><span class="p">(</span><span class="s">&#039;Procedencia de las nubes en agosto (%)&#039;</span><span class="p">)</span>
<span class="c">## Dibujamos los datos</span>
<span class="n">ax</span><span class="o">.</span><span class="n">bar</span><span class="p">(</span><span class="n">direcciones</span><span class="p">,</span> <span class="n">datos</span><span class="p">)</span>
<span class="c">## Colocamos las etiquetas del eje x</span>
<span class="n">ax</span><span class="o">.</span><span class="n">set_thetagrids</span><span class="p">(</span><span class="n">np</span><span class="o">.</span><span class="n">arange</span><span class="p">(</span><span class="mi"></span><span class="p">,</span> <span class="mi">360</span><span class="p">,</span> <span class="mi">45</span><span class="p">),</span> <span class="n">sectores</span><span class="p">,</span> <span class="n">frac</span> <span class="o">=</span> <span class="mf">1.1</span><span class="p">,</span> <span class="n">fontsize</span> <span class="o">=</span> <span class="mi">10</span><span class="p">)</span>
</pre>
        </div>
      </div>
    </div>
  </div>
  
  <div class="output_wrapper">
    <div class="output">
      <div class="output_area">
        <div class="prompt output_prompt">
          Out[4]:
        </div>
        
        <div class="output_text output_subarea output_pyout">
          <pre>
(&lt;a list of 16 Line2D ticklines objects&gt;,
 &lt;a list of 8 Text major ticklabel objects&gt;)
</pre>
        </div>
      </div>
      
      <div class="output_area">
        <div class="prompt">
        </div>
        
        <div class="output_png output_subarea ">
          <img src="http://new.pybonacci.org/images/2014/07/wpid-Dibujando_una_rosa_de_frecuencias_reloaded1.png" />
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
      Y listo.<br /> Saludos.
    </div>
  </div>
</div>