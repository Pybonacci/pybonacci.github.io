---
title: Sage: software matemático libre como alternativa
date: 2012-05-06T19:15:42+00:00
author: Juan Luis Cano
slug: sage-software-matematico-libre-como-alternativa
tags: cálculo simbólico, notebook, python, sage

Seguro que muchos de vosotros ya conocéis [Sage](http://sagemath.org/): un proyecto cuyo nada ambicioso objetivo es

> Crear una alternativa de código abierto, libre y viable a Magma, Maple, Mathematica y MATLAB.

Desde luego hay que admitir que como declaración de intenciones no está mal. Hechas las presentaciones, ¿qué más podemos decir sobre Sage?

[<img class="aligncenter size-full wp-image-373" title="Logo de Sage" alt="" src="http://pybonacci.org/wp-content/uploads/2012/05/sage-logo-new-l.png" width="488" height="130" srcset="https://pybonacci.org/wp-content/uploads/2012/05/sage-logo-new-l.png 488w, https://pybonacci.org/wp-content/uploads/2012/05/sage-logo-new-l-300x79.png 300w" sizes="(max-width: 488px) 100vw, 488px" />](http://pybonacci.org/wp-content/uploads/2012/05/sage-logo-new-l.png)

Sage comenzó en 2004 como un proyecto personal de [William Stein](http://www.wstein.org/), profesor de matemáticas en la Universidad de Washington, quien, [como explica en su blog](http://sagemath.blogspot.com.es/2009/12/mathematical-software-and-me-very.html), estaba frustrado por no poder solucionar las limitaciones de Magma al no ser un programa libre. Stein se dio cuenta de que, aunque crear un sistema como Magma o Maple llevaría años con un equipo de desarrolladores voluntarios partiendo de cero, _ya había numerosos paquetes de código abierto_ escritos en diferentes lenguajes enfocados a diversas áreas matemáticas. Así que decidió unir todos estos paquetes **utilizando Python** (en este momento son [cerca de 100](http://sagemath.org/links-components.html)) para crear un enorme software matemático para crear Sage. En esto se diferencia de otros proyectos como SymPy, del que ya [hemos](http://pybonacci.org/2012/04/04/introduccion-al-calculo-simbolico-en-python-con-sympy/) [hablado](http://pybonacci.org/2012/04/30/como-calcular-limites-derivadas-series-e-integrales-en-python-con-sympy/) en este blog.

<!--more-->

En este momento Sage ha visto más de 300 versiones y cuenta con [más de 200 colaboradores por todo el mundo](http://sagemath.org/development-map.html). Además, desde febrero de 2006 se han celebrado numerosos eventos, conocidos como [«Sage Days»](http://wiki.sagemath.org/Workshops), en los que los desarrolladores se han reunido para solucionar errores, implementar nuevas características, escribir documentación o hablar sobre el uso de Sage en educación.

Hablando de eventos, en España desde hace dos años se celebran cada verano las **Jornadas Sage/Python**, en las que se muestran las experiencias docentes que ya se están llevando a cabo con este programa en algunas universidades españolas y se explican ejemplos de aplicación. Este año se celebrarán las [III Jornadas Sage/Python en la Universidad de Vigo](http://webs.uvigo.es/sage2012/) los días 21 y 22 de junio de 2012 y estáis todos invitados 🙂

Sage dispone de una [documentación](http://sagemath.org/doc/) _enorme_ compuesta de tutoriales, guías y el [manual de referencia](http://sagemath.org/doc/reference/index.html). Solo por el tamaño de este último nos damos cuenta de la sorprendente amplitud de posibilidades que tiene este programa. Actualmente Sage le lleva la delantera a todos sus competidores no libres en cuanto a temas de matemática teórica, como pueden ser [curvas elípticas](http://sagemath.org/doc/reference/plane_curves.html) o [espacios de matrices](http://sagemath.org/doc/reference/matrices.html), y por supuesto es capaz de dibujar gráficos en 2D y en 3D y de crear componentes interactivos al estilo de Mathematica, con la diferencia que para compartirlos no necesitas el Mathematica Player: [solamente un navegador](http://aleph.sagemath.org/?z=eJyNkc9OhDAQxu88xZd4YAa7CKwe1qSJJ1_CmKYusFtDylqKvr5TQA970R6m8_c3X9NPGyhvo4IdLmer4HPOgqmpjQyNGndoUIBq7LAXp41L5hbTR4h0lWYUxVJslhQnUvMHafdP0kxJpN90JiItnozJEpYhEtk_UYEUCMMLYytsg9eNtKt57Sxg3yZa0xJnRrRoVGWdmXVVCg7Zk_OxC_YYs7brYUjaNEmXgthKrqasmBXWoVQ6qLSlfFAQw8yPGeRM5_GLBjdFcxnGSC_kRIFJr5zLaRYlwjW_P6NXHJPXjhn9GODgPIL1p47uK35VSJz30fmu1c92mDqF4ziMQec3VbXf933O_A33GX0V). En la Wikipedia podemos leer una extensa lista de características:

> Algunos de las muchas características de Sage incluyen:
> 
>   * Una interfaz gráfica (notebook) para la revisión y reutilización de entradas y salidas anteriores, incluyendo gráficas y notas de texto disponibles en la mayoría de los navegadores web incluyendo [Firefox](http://es.wikipedia.org/wiki/Firefox "Firefox"), [Opera](http://es.wikipedia.org/wiki/Opera_(navegador) "Opera (navegador)"), [Konqueror](http://es.wikipedia.org/wiki/Konqueror "Konqueror"), y [Safari](http://es.wikipedia.org/wiki/Safari "Safari").
> 
>   * Una línea de comandos basada en texto usando [iPython](http://es.wikipedia.org/wiki/IPython "IPython")
> 
>   * El [lenguaje de programación Python](http://es.wikipedia.org/wiki/Lenguaje_de_programaci%C3%B3n_Python "Lenguaje de programación Python"), que soporta expresiones en programación [orientada a objetos](http://es.wikipedia.org/wiki/Programaci%C3%B3n_orientada_a_objetos "Programación orientada a objetos") y [funcional](http://es.wikipedia.org/wiki/Programaci%C3%B3n_funcional "Programación funcional").
> 
>   * [Procesamiento paralelo](http://es.wikipedia.org/wiki/Computaci%C3%B3n_paralela "Computación paralela") usando tanto [procesadores de núcleo múltiple](http://es.wikipedia.org/w/index.php?title=Procesadores_de_n%C3%BAcleo_m%C3%BAltiple&action=edit&redlink=1 "Procesadores de núcleo múltiple (aún no redactado)") como [multiprocesadores simétricos](http://es.wikipedia.org/w/index.php?title=Multiprocesadores_sim%C3%A9tricos&action=edit&redlink=1 "Multiprocesadores simétricos (aún no redactado)").
> 
>   * Cálculo usando [Maxima](http://es.wikipedia.org/wiki/Maxima "Maxima") y [SymPy](http://es.wikipedia.org/wiki/SymPy "SymPy")
> 
>   * Álgebra lineal numérica usando [GSL](http://es.wikipedia.org/wiki/GNU_Scientific_Library "GNU Scientific Library"), [SciPy](http://es.wikipedia.org/wiki/SciPy "SciPy") y [NumPy](http://es.wikipedia.org/wiki/NumPy "NumPy")
> 
>   * Control interactivo de los cálculos
> 
>   * Librerías de funciones [elementales](http://es.wikipedia.org/wiki/Funci%C3%B3n_elemental "Función elemental") y [especiales](http://es.wikipedia.org/wiki/Funci%C3%B3n_especial "Función especial")
> 
>   * Gráficas en 2D y 3D tanto de funciones como de datos.
> 
>   * Herramientas de manipulación de datos y matrices.
> 
>   * Librerías de [estadística](http://es.wikipedia.org/wiki/Estad%C3%ADstica "Estadística") multivariable
> 
>   * Una caja de herramientas para añadir [interfaces de usuario](http://es.wikipedia.org/wiki/Interfaz_de_usuario "Interfaz de usuario") a cálculos y aplicaciones
> 
>   * Herramientas para [procesamiento de imágenes](http://es.wikipedia.org/wiki/Procesamiento_de_im%C3%A1genes "Procesamiento de imágenes") usando pylab así como Python
> 
>   * Herramientas para visualizar y analizar [gráficas](http://es.wikipedia.org/wiki/Gr%C3%A1fica "Gráfica")
> 
>   * Librerías para funciones de teoría de números
> 
>   * Filtros para importar y exportar datos, imágenes, vídeo, sonido, [CAD](http://es.wikipedia.org/wiki/CAD "CAD"), y [GIS](http://es.wikipedia.org/wiki/GIS "GIS")
> 
>   * Soporte para [números complejos](http://es.wikipedia.org/wiki/N%C3%BAmeros_complejos "Números complejos"), [aritmética de precisión arbitraria](http://es.wikipedia.org/w/index.php?title=Aritm%C3%A9tica_de_precisi%C3%B3n_arbitraria&action=edit&redlink=1 "Aritmética de precisión arbitraria (aún no redactado)"), y computación simbólica de funciones donde esto sea apropiado.
> 
>   * Embeber Sage en documentos [LaTeX](http://es.wikipedia.org/wiki/LaTeX "LaTeX")<span style="font-size:11px;">.</span>
> 
>   * Interfaces a otro software como [Mathematica](http://es.wikipedia.org/wiki/Mathematica "Mathematica"), [Magma](http://es.wikipedia.org/wiki/Magma "Magma") y [Maple](http://es.wikipedia.org/wiki/Maple "Maple"), que le permite a los usuarios combinar software y comparar resultados y desempeño.

¿Alguien habló de interfaz gráfica? ¡Sí! Sage tiene una interfaz a imitación de los «notebooks» de Mathematica que funciona a través del navegador, y que además permite la edición colaborativa de documentos. Puedes utilizarla con el programa, montar tu propio servidor o crear una cuenta en el [servidor público de Sage](http://www.sagenb.org/) para empezar a experimentar.<figure id="attachment_378" style="width: 420px" class="wp-caption aligncenter">

[<img class=" wp-image-378" title="Interfaz gráfica de Sage" alt="" src="http://pybonacci.org/wp-content/uploads/2012/05/2012-05-06-195446_1366x768_scrot.png" width="420" height="236" srcset="https://pybonacci.org/wp-content/uploads/2012/05/2012-05-06-195446_1366x768_scrot.png 1366w, https://pybonacci.org/wp-content/uploads/2012/05/2012-05-06-195446_1366x768_scrot-300x168.png 300w, https://pybonacci.org/wp-content/uploads/2012/05/2012-05-06-195446_1366x768_scrot-1024x575.png 1024w, https://pybonacci.org/wp-content/uploads/2012/05/2012-05-06-195446_1366x768_scrot-1200x674.png 1200w" sizes="(max-width: 420px) 100vw, 420px" />](http://pybonacci.org/wp-content/uploads/2012/05/2012-05-06-195446_1366x768_scrot.png)<figcaption class="wp-caption-text">Ejemplo de cómo se ve un «notebook» en la interfaz de Sage (vista pública en http://sagenb.org/home/pub/3319/)</figcaption></figure> 

Es complicado hacer una introducción a este programa porque es bastante inabarcable, pero espero que te haya resultado interesante. Si te apetece saber más cosas sobre Sage, puedes consultar [este «notebook» público](http://www.sagenb.org/home/pub/873/) que explica algunas de sus posibilidades (e incluso editarlo tú mismo). O puedes estar atento a futuras publicaciones en Pybonacci 😉

¡Un saludo!