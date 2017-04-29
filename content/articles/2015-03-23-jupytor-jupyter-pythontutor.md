---
title: tutormagic: Jupyter + pythontutor
date: 2015-03-23T19:40:47+00:00
author: Kiko Correoso
slug: jupytor-jupyter-pythontutor
tags: enseñanza, ipython, jupyter, pythontutor

 

<div>
  <div>
  </div>
  
  <div>
    <div>
      Esta será una microentrada para presentar una extensión para el notebook que estoy usando en un curso interno que estoy dando en mi empresa.<br /> Si a alguno más os puede valer para mostrar cosas básicas de Python (2 y 3, además de Java y Javascript) para muy principiantes me alegro.</p>
    </div>
  </div>
</div>

<div>
  <div>
  </div>
  
  <div>
    <div>
      <h1 id="Nombre-en-clave:-Jupytor">
        Nombre en clave: tutormagic<a class="anchor-link" href="#Nombre-en-clave:-Jupytor">&#182;</a>
      </h1>
    </div>
  </div>
</div>

<div>
  <div>
  </div>
  
  <div>
    <div>
      Esta extensión lo único que hace es embeber dentro de un IFrame la página de <a href="http://www.pythontutor.com">pythontutor</a> usando el código que hayamos definido en una celda de código precedida de la <em>cell magic</em> <code>%%tutor</code>.<br /> Como he comentado anteriormente, se puede escribir código Python2, Python3, Java y Javascript, que son los lenguajes soportados por pythontutor.</p>
    </div>
  </div>
</div>

<div>
  <div>
  </div>
  
  <div>
    <div>
      <h1 id="Ejemplo">
        Ejemplo<a class="anchor-link" href="#Ejemplo">&#182;</a>
      </h1>
    </div>
  </div>
</div>

<div>
  <div>
  </div>
  
  <div>
    <div>
      Primero deberemos instalar la extensión. Está disponible en pypi por lo que la podéis instalar usando <code>pip install tutormagic</code>. Una vez instalada, dentro de un notebook de IPython la deberías cargar usando:</p>
    </div>
  </div>
  
  <div>
    <div>
      <div>
        <div>
          <div class=" highlight hl-ipython3">
            <pre><span class="o">%</span><span class="k">load_ext</span> tutormagic
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
        </div>
      </div>
    </div>
  </div>
  
  <div>
    <div>
      <div>
        Una vez hecho esto ya deberiamos tener disponible la <em>cell magic</em> para ser usada. Podéis ver un ejemplo en <a href="http://nbviewer.ipython.org/github/Pybonacci/notebooks/blob/master/tutormagic.ipynb">este notebook</a>.
      </div>
    </div>
  </div>
</div>

<div>
</div>

<div>
</div>

<div>
  <div>
  </div>
  
  <div>
    <div>
      <h1 id="Y-eso-es-todo">
        Y eso es todo<a class="anchor-link" href="#Y-eso-es-todo">&#182;</a>
      </h1>
    </div>
  </div>
</div>

<div>
  <div>
  </div>
  
  <div>
    <div>
      Lo dicho, espero que sea útil para alguien.</p> 
      
      <ul>
        <li>
          <a href="https://pypi.python.org/pypi/tutormagic">tutormagic en pypi</a>.
        </li>
        <li>
          <a href="https://github.com/kikocorreoso/tutormagic">tutormagic en github</a>
        </li>
      </ul>
      
      <p>
        Saludos.
      </p>
    </div>
  </div>
</div>