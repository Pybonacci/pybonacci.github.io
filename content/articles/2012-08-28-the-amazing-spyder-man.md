---
title: The amazing Spyder, man!!!
date: 2012-08-28T18:11:06+00:00
author: Kiko Correoso
slug: the-amazing-spyder-man
tags: IDEs, python, spyder, spyderlib

Spyder es la abreviación de Scientific PYthon Development EnviRonment. Según la documentación oficial, Spyder es un potente entorno de desarrollo interactivo para Python con edición avanzada, ‘testeo’ interactivo y capacidades de introspección y depuración (debugging) y, esto es lo que nos interesa, un entorno de computación numérica gracias al soporte de IPython y de populares librerías como numpy, scipy y matplotlib (todas conocidas ya por aquí).

Se puede instalar tanto en Linux como en Windows (y en Mac para los amantes de Alcatraz). En el siguiente enlace podéis ver [documentación para la instalación y los requerimientos](http://code.google.com/p/spyderlib/wiki/Installation) previos para poder instalarlo.

En un vistazo general podemos ver que es muy adaptable a nuestras necesidades (o manías) permitiendo:

  * definir accesos rápidos,
  * Gestionar el PYTHONPATH de manera visual

[<img class="aligncenter size-full wp-image-787" title="pythonpath" alt="" src="http://pybonacci.org/wp-content/uploads/2012/08/pythonpath.png" width="502" height="329" srcset="https://pybonacci.es/wp-content/uploads/2012/08/pythonpath.png 502w, https://pybonacci.es/wp-content/uploads/2012/08/pythonpath-300x196.png 300w" sizes="(max-width: 502px) 100vw, 502px" />](http://pybonacci.org/wp-content/uploads/2012/08/pythonpath.png)

  * Acceso a la documentación de las librerías más importantes (Numpy, Scipy, Matplotlib,...) desde la ayuda del propio IDE
  * Acceso directo a herramientas (y documentación) Qt.
  * Configuración del coloreado de la sintáxis
  * Podemos colocar los paneles como mejor nos convenga. En general, yo lo configuro con un explorador de archivos a la izquierda, el editor a la derecha y abajo cosas útiles como consolas, el historial, y el explorador de variables:[<img class="aligncenter  wp-image-788" title="IDE" alt="" src="http://pybonacci.org/wp-content/uploads/2012/08/ide.png" width="560" height="355" srcset="https://pybonacci.es/wp-content/uploads/2012/08/ide.png 1616w, https://pybonacci.es/wp-content/uploads/2012/08/ide-300x190.png 300w, https://pybonacci.es/wp-content/uploads/2012/08/ide-1024x650.png 1024w, https://pybonacci.es/wp-content/uploads/2012/08/ide-1200x761.png 1200w" sizes="(max-width: 560px) 100vw, 560px" />](http://pybonacci.org/wp-content/uploads/2012/08/ide.png)
  * Pero con el mismo ratón se puede recolocar todo de forma sencilla y se puede elegir que aparece en la pantalla desde el menú ‘view | Windows and toolbars’:

<p style="text-align:center;">
  <a href="http://pybonacci.org/wp-content/uploads/2012/08/ideconfigurable.png"><img class="aligncenter  wp-image-789" title="IDEconfigurable" alt="" src="http://pybonacci.org/wp-content/uploads/2012/08/ideconfigurable.png" width="560" height="350" srcset="https://pybonacci.es/wp-content/uploads/2012/08/ideconfigurable.png 1680w, https://pybonacci.es/wp-content/uploads/2012/08/ideconfigurable-300x187.png 300w, https://pybonacci.es/wp-content/uploads/2012/08/ideconfigurable-1024x640.png 1024w, https://pybonacci.es/wp-content/uploads/2012/08/ideconfigurable-1200x750.png 1200w" sizes="(max-width: 560px) 100vw, 560px" /></a>
</p>

Puedes ver [más pantallazos en el siguiente enlace](http://code.google.com/p/spyderlib/wiki/Screenshots).

El editor en sí permite resaltar código Python, C/C++ y Fortran, completado de código, permite analizar el código con pylint, depurar con pdb (o winpdb), avisos y errores en tiempo real con pyflakes,… Lo mínimo que lleva hoy en día cualquier editor potente.

<!--more-->

Además se pueden correr consolas (python y ipython o terminales de línea de comandos del propio sistema operativo) como procesos separados, permite inspeccionar las variables, importar datos en  varios formatos como ficheros de datos numpy (npy), ficheros de datos matlab (mat), csv, HDF5 (h5),…, permite guardar datos de una variable de la sesión en formato spydata (formato interno de spyder), matlab o hdf5, posibilidad de ver el historial, permite búsquedas de texto con resaltado de todas las ocurrencias [y más](http://code.google.com/p/ spyderlib/wiki/Features).

La documentación online la tenéis en: [http://packages.python.org/spyder](http://packages.python.org/spyder/)/

El blog del equipo de desarrollo está en: <http://spyder-ide.blogspot.com.es/>

La lista de correo está en: <http://groups.google.com/group/spyderlib>

Y, por supuesto, la página web, está en: <http://code.google.com/p/spyderlib/>

En definitiva, Spyder es un IDE que tiene todo lo necesario para que nuestros desarrollos sean más cómodos y además viene con las baterías científicas de python a tope de energía.