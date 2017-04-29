---
title: SyntaxError: more than 255 arguments
date: 2014-10-12T16:01:03+00:00
author: Kiko Correoso
slug: syntaxerror-more-than-255-arguments
tags: CPython, especificación de Python, implementación

Para el que no lo sepa, las funciones en CPython tienen una limitación de 255 argumentos ([*] leed más abajo para más información). Mirad la siguiente pieza de código C en [ast.c](https://hg.python.org/cpython/file/433048fd4206/Python/ast.c#l2457) en el repositorio oficial de CPython:

<pre class="language-c"><code class="language-c" data-language="c">    if (nargs + nkeywords + ngens > 255) {
        ast_error(c, n, "more than 255 arguments");
        return NULL;
    }</code></pre>

Y probad, por ejemplo, lo siguiente en vuestra consola/editor de Python favorito:

<pre class="language-python"><code class="language-python" data-language="python">def fn(*args):
    pass

fn(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,
   21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,
   39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,
   57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,
   75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,
   93,94,95,96,97,98,99,100,101,102,103,104,105,106,
   107,108,109,110,111,112,113,114,115,116,117,118,
   119,120,121,122,123,124,125,126,127,128,129,130,
   131,132,133,134,135,136,137,138,139,140,141,142,
   143,144,145,146,147,148,149,150,151,152,153,154,
   155,156,157,158,159,160,161,162,163,164,165,166,
   167,168,169,170,171,172,173,174,175,176,177,178,
   179,180,181,182,183,184,185,186,187,188,189,190,
   191,192,193,194,195,196,197,198,199,200,201,202,
   203,204,205,206,207,208,209,210,211,212,213,214,
   215,216,217,218,219,220,221,222,223,224,225,226,
   227,228,229,230,231,232,233,234,235,236,237,238,
   239,240,241,242,243,244,245,246,247,248,249,250,
   251,252,253,254,255,256)
</code></pre>

El resultado debería ser similar al título de esta entrada:

<pre class="language-python"><code>SyntaxError: more than 255 arguments</code></pre>

Parece que esto es una limitación de la implementación CPython y no es una especificación del lenguaje. Podéis [leer esta conversación](http://bugs.python.org/issue12844) en la que Raymond Hettinger [comenta](http://bugs.python.org/issue12844#msg142998) que Guido lo considera una limitación arbitraria y que debería ser eliminada en algún momento de CPython (pero ahí sigue en mi CPython3.4). En Pypy lo han implementado exactamente igual (_[offtopic] ¿deberían respetar la implementación oficial hasta en cosas que se podrían mejorar? [/offtopic]_)

[*] Por lo visto, es una [limitación del _bytecode_ compilado](http://stackoverflow.com/questions/714475/what-is-a-maximum-number-of-arguments-in-a-python-function/8932175#8932175) cuando llamamos a una función (no es un problema de la función en sí, [pero sí de la llamada a la función](http://ajhekman.com/2012/08/25/use-more-than-255-columns-in-sqlalchemy/)).

Como explican en el último enlace del párrafo anterior, esta limitación se puede sortear de forma muy sencilla usando `*args` y `**kwargs`:

<pre class="language-python"><code class="language-python" data-language="python">argumentos = (1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,
   21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,
   39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,
   57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,
   75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,
   93,94,95,96,97,98,99,100,101,102,103,104,105,106,
   107,108,109,110,111,112,113,114,115,116,117,118,
   119,120,121,122,123,124,125,126,127,128,129,130,
   131,132,133,134,135,136,137,138,139,140,141,142,
   143,144,145,146,147,148,149,150,151,152,153,154,
   155,156,157,158,159,160,161,162,163,164,165,166,
   167,168,169,170,171,172,173,174,175,176,177,178,
   179,180,181,182,183,184,185,186,187,188,189,190,
   191,192,193,194,195,196,197,198,199,200,201,202,
   203,204,205,206,207,208,209,210,211,212,213,214,
   215,216,217,218,219,220,221,222,223,224,225,226,
   227,228,229,230,231,232,233,234,235,236,237,238,
   239,240,241,242,243,244,245,246,247,248,249,250,
   251,252,253,254,255,256)

fn(*argumentos) #ahora no daría un error de sintaxis</code></pre>

No es que sea algo muy importante y no es habitual usar más de 255 argumentos en una función pero me ha parecido curioso, lo he investigado un poco y lo pongo aquí por si a alguien más le puede interesar.

Saludos.

P.D.: Como siempre, si algo de lo que he escrito es erróneo, por favor, comentadlo y lo actualizo tan rápidamente como pueda.