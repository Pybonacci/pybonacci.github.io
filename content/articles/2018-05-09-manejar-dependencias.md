---
title: Manejar dependencias y entornos de desarrollo en Python
date: 2018-05-09T18:00:00+00:00
author: Daniel Rodriguez
slug: manejar-dependencias-python

aka. pip, conda, pipenv, pyenv, y mas! ¿Quéå uso?

Paquetes de Python, los hay para todos los gustos, muchas industrias (web, ciencia, datos y más), con buen soporte tanto de la comunidad como por empresas grandes en cada sector y en general te permiten resolver muchos problemas rápidamente y moverte al siguiente.

Manejar estos paquetes y dependencias es parte natural de un proyecto de software y como es de esperarse en una comunidad tan grande y variada como lo es la de Python no existe solo una solución sino al contrario muchas (¡lo cual es bueno!) que se adaptan a diferentes necesidades de diferentes usuarios.

Tantas opciones también pueden generar confusión al momento de elegir qué herramientas usar y aprender. Para la muestra un gran comic de XKCD que muestra lo que puede pasar.

![¡Ayuda!](https://imgs.xkcd.com/comics/python_environment.png "https://xkcd.com/1987/")

Veamos cuales son las opciones que existen, para qué sirven y algo de historia. Lo he dividido en dos secciones: manejadores de paquetes y entornos virtuales.

## Manejadores de paquetes

O como instalar dependencias en Python.

### pip

pip es el instalador de paquetes por defecto y oficial que viene con Python. Si tienes Python (una version relativamente moderna: Python 2 >=2.7.9 o Python 3 >=3.4) ya tienes pip y puedes instalar paquetes del PyPI: Python Package Index ([https://pypi.org](https://pypi.org)), el repositorio oficial de Python donde cualquier persona puede crear una cuenta y subir sus propios paquetes para que puedan ser usados por la comunidad.

Instalar un paquete usando pip es muy sencillo, solo ejecuta: `pip install <paquete>`, por ejemplo: `pip install pandas`.

### conda

[Conda](https://conda.io/docs/) es otra opción para instalar paquetes de Python que no es oficial de Python y su desarrollo y mantenimiento lo provee otra empresa [Anaconda](https://www.anaconda.com/). Conda se ha posicionado como una de las formas de instalar paquetes por defecto en la comunidad científica y de análisis de datos en Python. De la misma forma que pip instala paquetes de Python que vienen de PyPI, conda instala paquetes de conda que viene de su propio repositorio de paquetes.

Instalar paquetes es igual de fácil que con pip, solo ejecuta `conda install <paquete>`, por ejemplo: `conda install pandas`.

El repositorio de conda es independiente del repositorio oficial de Python y no se encuentran todos los paquetes de Python que están en PyPI pero casi con total seguridad vas a encontrar todas las librerías científicas de Python como Numpy, Scipy, Pandas y cientos más.

Esta es una de las grandes diferencias de conda, que a su vez es una de sus grandes virtudes porque conda permite no solo manejar paquetes de Python además permite manejar paquetes de cualquier lenguaje de programación, incluyendo R, Scala y otros. Algunos de estos están disponibles en los repositorios de anaconda y otros los mantiene la comunidad en [anaconda.org](anaconda.org).

Para usar conda tienes que instalar la [distribución de Anaconda](https://www.anaconda.com/download/) que está disponible para Windows, Mac y Linux. Todas las distribuciones de Anaconda vienen con conda y puedes empezar a usarlo inmediatamente. Una ventaja de la distribución de Anaconda es que viene con más de 100 paquetes muy populares de Python así que puedes empezar a codear en Python.

### ¿Por qué otra opción para manejar paquetes? 

Esta es una pregunta muy frecuente y la respuesta requiere un poco de historia y es larga. En resumen las necesidades de la comunidad científica de Python no estaban bien servidas por lo que hacía Python en su momento y se recomendó que existiera una solución independiente para resolver los problemas existían en esos momentos.

¿Que problemas eran esos que pip no podía resolver en su momento? En general se resume en que la mayoría de paquetes de la comunidad científica de Python están escritos en C, C++ o Fortran con bindings a Python. Estos paquetes necesitan ser compilados para poder ser usados y compilar las librerías base como lo son Numpy, Scipy y Pandas es un proceso largo, complicado y depende de la plataforma en que se estén ejecutando.

En su momento Continuum Analytics (ahora Anaconda, la empresa) decidió resolver estos problemas y creó la distribution de Anaconda y conda. Y resolvió estos problemas tan bien que gran parte de la comunidad de datos en Python adoptó conda y Anaconda como la forma de manejar paquetes por defecto. Este es el motivo por el cual se ve mucho conda en la comunidad científica pero no tanto fuera de ella, paquetes de la comunidad web como Flask y Django no se ven tan beneficiados por conda como Numpy y Pandas.

Un artículo con mas información lo puedes [encontrar acá].(https://jakevdp.github.io/blog/2016/08/25/conda-myths-and-misconceptions/#Myth-#4:-Creating-conda-in-the-first-place-was-irresponsible-&-divisive).

**Estos problemas aun existen?**

Desde que se creó conda y Anaconda han habido muchos progresos en la forma en que se manejan paquetes en Python, uno que ayudó bastante fue la introducción de wheels. Básicamente esto permitió agregar paquetes compilados a PyPI en una forma similar a lo que provee un paquete de conda. Dado que el estándar de wheels y su adopción ha tomado mucho tiempo conda ganó gran popularidad y se convirtió en una especie de estándar.

## Entornos virtuales

Ya sabemos cómo instalar paquetes con pip o conda. Ahora ¿qué es esto de entornos virtuales?

Imagínate la situación en que tienes un proyecto en tu empresa o universidad que usa la versión 0.20 de pandas. Ahora imagina que tienes otro proyecto, tal vez uno en el que trabajas en tu tiempo libre, en el que quieres usar la última versión disponible de pandas, digamos 0.22. Ahora imagina la misma situación pero con no solo un paquete sino 10 o 20 e, incluso, con diferentes versiones de Python, una que utiliza Python 2.7, otro Python 3.6 y otro con Python 3.7. ¿Cómo haces para trabajar en varios proyectos en el mismo ordenador?

Este problema es lo que solucionan los entornos virtuales, o virtual environments, y de la misma forma que hay dos grandes opciones para instalar paquetes tenemos dos opciones (con extras) para crear entornos virtuales, una oficial de Python y otra en conda.

### virtualenv

[virtualenv](https://virtualenv.pypa.io/) es una herramienta de Python para crear entornos virtuales. Para instalarla solo tienes que ejecutar: `pip install virtualenv` . Ya con esto puedes empezar a crear los entornos virtuales, por ejemplo: `virtualenv ENV` . Donde ENV es un directorio donde se va a instalar en entorno virtual que incluye una instalación de Python independiente. Para más información mirar la guia completa que incluye como activar los environments aca: [https://virtualenv.pypa.io](https://virtualenv.pypa.io/).

Dado que virtualenv empezó como una herramienta no oficial de Python y funciona con una serie de hacks se crearon herramientas que complementan e incluso unas alternativas:

- [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/): Una serie de scripts alrededor de virtualenv para hacer la vida un poco más fácil, si usas virtualenv usa virtualenvwrapper. Solo funciona en Linux con ciertas shells, [documentacion mas completa acá](https://virtualenvwrapper.readthedocs.io/en/latest/install.html).
- [virtualenvwrapper-win](https://pypi.python.org/pypi/virtualenvwrapper-win): Lo mismo que virtualenvwrapper para Windows.
- [venv](https://docs.python.org/3/library/venv.html): Desde Python 3.3 en adelante, Python incluye una herramienta oficial que no necesita ser instalada para crear virtual environments.
- pyvenv: Era un script al que ayudaba a venv pero ha sido descontinuado desde Python 3.6 - no utilices pyvenv, utiliza solo venv

### pyenv

[pyenv](https://github.com/pyenv/pyenv) es una herramienta que permite instalar y mantener varias versiones de Python en un mismo ordenador, funciona de una manera similar a virtualenv pero incluso permite instalar Anaconda. Recomiendo utilizarla si mantienes paquetes de Python que quieres probar y construir en varias versiones de Python incluyendo paquetes instalados mediante pip o conda.

### pipenv

[pipenv](https://github.com/pypa/pipenv) es una herramienta relativamente nueva que moderniza la forma en que Python maneja dependencias, incluye un resolvedor de dependencias completo como en conda, manejo de entornos virtuales, lock files como en la mayoría de lenguajes modernos y más. pipenv es oficial de Python y solo tienes que ejecutar lo siguiente para instalarla: `pip install pipenv`. En mi opinión puede llegar a ser el futuro de manejar dependencias en Python pero aún no está claro que tan grande será su adopción dado que entra a un terreno competido.

Puedes encontrar una excelente guía para pipenv en ingles aca: [https://realpython.com/pipenv-guide](https://realpython.com/pipenv-guide/)

### conda

De la misma forma que existen virtual environment en Python también existen en conda como conda environments. En este caso no tienes que instalar nada ya que vienen incluidos en conda y puedes crear una ejecutando: `conda create -n ENV` o `conda create -p PATH_TO_ENV` donde `ENV` es el nombre del environment y `PATH_TO_ENV` es un directorio, igual que en virtualenv. Para una guia completa mira la [documentación](https://conda.io/docs/using/envs.html).

## Que me recomiendas?

Si eres un usuario completamente nuevo en Python recomiendo [Anaconda](https://www.anaconda.com/download/), simplemente descárgalo y empieza a aprender Python. Anaconda tiene muchas librerías incluidas y puedes instalar más de los repositorios oficiales. Si necesitas más paquetes recomiendo utilizar el repositorio de [conda-forge](https://github.com/conda-forge/) en donde la comunidad ha creado más de 3000 paquetes de Python y otros lenguajes.

Si ya eres un usuario más avanzado, que busca tener los últimos paquetes el dia que salen y que busca usar exactamente lo que los desarrolladores publican entonces debes usar pip dado que hay un lag (usualmente menor a un par de días) en lo que sale un nuevo release y en lo que Anaconda u otras personas en la comunidad publican un paquete de conda.

**¿Qué uso yo?**

En caso de que te preguntes qué uso como trabajo: yo utilizo los dos, tanto conda como pip.

Utilizó Anaconda como mi versión de Python y uso conda para manejar los entornos virtuales dado que me parecen superiores a los creados por virtualenv. En general también utilizó paquetes de conda pero a veces sucede que debo instalar paquetes usando de pip. En otras ocasiones puede que tenga un conda environment con solo Python y después instale todos los paquetes de ese entorno virtual usando pip. Por ejemplo, me sucede esto con tensorflow.

## Referencias

1. https://stackoverflow.com/questions/38217545/what-is-the-difference-between-pyenv-virtualenv-anaconda/39928067
1. https://www.reddit.com/r/learnpython/comments/4hsudz/pyvenv_vs_virtualenv/
1. https://docs.python.org/3/library/venv.html



