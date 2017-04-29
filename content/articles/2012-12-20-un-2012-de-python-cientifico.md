---
title: Un 2012 de Python científico
date: 2012-12-20T15:05:31+00:00
author: Kiko Correoso
slug: un-2012-de-python-cientifico

Primero de todo, lo más importante, ¡¡¡ha nacido Pybonacci!!!! Un blog dedicado a hablar del uso de Python en el ámbito científico y en español. Si no lo conocéis aún, podéis visitarlo en <http://pybonacci.org> 🙂

  * Blog (+Twitter, +Fb, +G+) nacido en marzo de 2012
  * Más de 60 artículos publicados
  * Más de 30.000 visitas recibidas
  * Tres autores (esperamos que aumenten en el 2013)
  * Más de 2000 tuits

Venga, hablando en serio, os resumo lo que ha sido este año. Primero veamos las novedades de la base de lo que es Python en el entorno científico, la trinidad: NumPy, matplotlib y SciPy:

**NUMPY**

  * Ha salido la versión 1.6.2 de NumPy y se [espera que en breve salga la versión 1.7.0 que ahora mismo está en beta](https://github.com/numpy/numpy/issues/milestones?state=open&with_issues=yes). La versión 1.6.2 de NumPy es compatible con Python 3.2 y la 1.7.0 será compatible con Python 3.3.

**MATPLOTLIB**

  * Lo más destacable, por desgracia, fue la [muerte de John Hunter](http://numfocus.org/johnhunter/), creador de matplotlib, de forma rápida y repentina. Por otra parte, este año salió la versión 1.2 totalmente compatible con Python 3.x, [entre otras muchas novedades](http://matplotlib.org/1.2.0/users/whats_new.html#new-in-matplotlib-1-2). Ya hablamos sobre matplotlib 1.2 en nuestro artículo sobre [líneas de corriente en Python](http://pybonacci.org/2012/11/13/visualizando-lineas-de-corriente-en-python-con-matplotlib/ "Visualizando líneas de corriente en Python con matplotlib").

**SCIPY**

  * Ha salido la [versión 0.11](http://sourceforge.net/projects/scipy/files/scipy/0.11.0/) que también es compatible con Python 3.2. Se ha incluido un submódulo dentro de scipy.sparse, se han introducido mejoras en scipy.optimize, scipy.linalg, scipy.interpolate, ...

Los tres proyectos se han movido a GitHub, junto con otros, y el desarrollo ha crecido exponencialmente. ¡¡Esto son buenas noticias!!

<!--more-->

El creador de numpy, Travis Oliphant, ha creado [Continuum](http://www.continuum.io/) que están dando un gran espaldarazo a la comunidad científica creando una [serie de herramientas](http://continuum.io/developer-resources.html) que son más que interesantes y que durante el 2013 darán mucho que hablar. [Blaze](https://github.com/ContinuumIO/blaze), por ejemplo, acaba de recibir una [inversión de $3.000.000](http://technicaldiscovery.blogspot.com.es/2012/12/passing-torch-of-numpy-and-moving-on-to.html) por parte de la [DARPA](www.darpa.mil/). [numba](https://github.com/numba/numba) parece algo excitante para gente que necesita acelerar sus cálculos, y de hecho en Pybonacci puedes leer nuestro [artículo sobre numba](http://pybonacci.org/2012/08/21/probando-numba-compilador-para-python-basado-en-llvm/ "Probando numba: compilador para Python basado en LLVM").

Siguiendo con otras herramientas:

**IPYTHON**

Sin duda, este ha sido un año muy importante para [IPython](http://ipython.org/):

  * Ha salido la versión 0.13 siendo totalmente funcional con Python 3.

  * Acaban de recibir una [donación de 1.15 millones de dólares de la Sloan Foundation](http://ipython.org/sloan-grant.html).

  * [Software Carpentry](http://software-carpentry.org/) ha adoptado el IPython notebook para todos sus cursos.

  * Su notebook está revolucionando el modo de crear ciencia (entre otras cosas) y se esperan muchísimas novedades para el 2013 como introducir gráficos interactivos con [flot](http://www.flotcharts.org/) o [D3](http://d3js.org/) <modo pataleta ON>¿por qué solo existe JS para el navegador? No quiero aprender JS para hacer esas cosas tan chulas que se hacen con JS en el navegador<modo pataleta OFF>.

¿Que aun no has probado IPython? Lo puedes probar online desde [PythonAnywhere](https://www.pythonanywhere.com/try-ipython/). Puedes leer nuestra [introducción a IPython](http://pybonacci.org/2012/07/02/introduccion-a-ipython-mucho-mas-que-un-interprete-de-python/ "Introducción a IPython: mucho más que un intérprete de Python") o nuestro artículo sobre [el notebook de IPython](http://pybonacci.org/2012/11/02/el-notebook-de-ipython/ "El notebook de IPython").

**PANDAS**

[Pandas](https://github.com/pydata/pandas) se está mostrando muy capaz para añadir cosas que existen en R y que Python no tenía como el DataFrame.

  * Esta semana ha salido la versión 0.10, también compatible con Python 3 (por lo menos hasta 3.2, 3.3 no estoy muy seguro).
  * Se ha publicado un [libro en O'Reilly](http://shop.oreilly.com/product/0636920023784.do) donde se da buena cuenta de la librería además de mostrar el uso de Python como herramienta de análisis de datos.

**SYMPY**

La biblioteca para cálculo simbólico también pasa por un buen momento. Para mí ha sido un descubrimiento de este año, después de no tocar cosas de estas desde mis estudios usando, en aquellos momentos, los inefables maple o mathematica.

  * Ha salido la versión 0.7.2 hace apenas un par de meses.
  * Ya es [compatible con Python 3.3 y con PyPy 1.9](https://github.com/sympy/sympy/wiki/Release-Notes-for-0.7.2). ¡¡¡La combinación pypy + sympy puede ser algo muy interesante!!!

¿Has leído ya nuestra [introducción a SymPy](http://pybonacci.org/2012/04/04/introduccion-al-calculo-simbolico-en-python-con-sympy/ "Introducción al Cálculo Simbólico en Python con SymPy") o nuestro tutorial sobre [cómo calcular límites, derivadas, series e integrales con SymPy](http://pybonacci.org/2012/04/30/como-calcular-limites-derivadas-series-e-integrales-en-python-con-sympy/ "Cómo calcular límites, derivadas, series e integrales en Python con SymPy")?

**CONFERENCIAS**

Ha habido muchas este año y parece que va en aumento el interés por hacer más:

  * La presencia de la rama científica de Python en la PyCon US de este año ha sido muy notable.
  * Este año se ha alcanzado la 11ª SciPy en los EEUU, la 5ª EuroScipy y la 3ª Scipy.in.
  * Se han organizado dos talleres sobre Python en el ámbito del «big data» (nueva «buzzword»), uno hospedado por Google en su sede de Mountain View y otro en NY que, por lo visto, ha sido un tremendo éxito.
  * Existen conferencias más focalizadas que ya empiezan a ser «veteranas» como la que organiza la [American Meteorological Society](http://annual.ametsoc.org/2013/index.cfm/programs-and-events/conferences-and-symposia/third-symposium-on-advances-in-modeling-and-analysis-using-python/), o la [pyHPC](http://www.dlr.de/sc/desktopdefault.aspx/tabid-8028/13765_read-34936/), ...
  * Habrá una PyData dentro de la PyCon US del 2013.

En Pybonacci hemos hecho resúmenes o listados de vídeos de muchas de estas conferencias: puedes leer por ejemplo nuestro [repaso a la EuroSciPy 2012](http://pybonacci.org/2012/09/17/repaso-a-la-euroscipy-2012/ "Repaso a la EuroScipy 2012") o la [recopilación de vídeos del PyData NYC](http://pybonacci.org/2012/10/31/recopilacion-del-pydata-nyc-2012/ "Recopilación del PyData NYC 2012"), entre otros 🙂

**Libros**

Este ha sido un año de gran proliferación de libros hablando sobre bibliotecas del ecosistema científico pythonico:

  * [SciPy and NumPy](http://www.amazon.com/SciPy-NumPy-Developers-Eli-Bressert/dp/1449305466/ref=sr_1_1?s=books&ie=UTF8&qid=1355998493&sr=1-1)
  *  [Machine learning in action](http://www.amazon.com/Machine-Learning-Action-Peter-Harrington/dp/1617290181/ref=la_B0088R1OMA_1_1?ie=UTF8&qid=1355998558&sr=1-1)
  * [Think complexity](http://www.amazon.com/Think-Complexity-Science-Computational-Modeling/dp/1449314635/ref=sr_1_2?s=books&ie=UTF8&qid=1355998637&sr=1-2)
  * [Practical Computer Vision with SimpleCV: The Simple Way to Make Technology See](http://www.amazon.com/Practical-Computer-Vision-SimpleCV-Technology/dp/1449320368/ref=sr_1_1?s=books&ie=UTF8&qid=1355998843&sr=1-1)
  * [NumPy Cookbook](http://www.amazon.com/NumPy-Cookbook-Ivan-Idris/dp/1849518920/ref=sr_1_3?s=books&ie=UTF8&qid=1355998888&sr=1-3&keywords=numpy)
  * [Python for data analysis](http://www.amazon.com/Python-Data-Analysis-Wes-McKinney/dp/1449319793/ref=sr_1_4?s=books&ie=UTF8&qid=1355998888&sr=1-4&keywords=numpy)
  * [Programming Computer Vision with Python: Tools and algorithms for analyzing images](http://www.amazon.com/Programming-Computer-Vision-Python-algorithms/dp/1449316549/ref=sr_1_7?s=books&ie=UTF8&qid=1355998888&sr=1-7&keywords=numpy)
  * [Think Bayes](http://www.greenteapress.com/thinkbayes/thinkbayes.pdf)

**Otras historias**

  * Se ha creado la fundación NumFocus con el propósito de promocionar el uso de cálculos accesibles y reproducibles en entornos científicos y tecnológicos.
  * Salen cosas nuevas interesantes como [Julia](http://julialang.org/), de las que se pueden aprender cosas nuevas.
  * La velocidad del lenguaje resulta crítica en ciertos momentos y, por suerte, tenemos herramientas que permiten seguir disfrutando de la simplicidad de la sintaxis de Python con velocidades cercanas a Fortran y/o C como cython, theano, numpypy, numexpr, el ya citado numba, [mypy](http://www.mypy-lang.org/) (algunas muy experimentales y que ya veremos en qué acaban).
  * Este año ha habido una explosión de cursos online de todo tipo (Coursera, Khan Academy, Udacity, edX, ...) y en muchos de ellos se ha elegido Python para dar las lecciones.
  * También, páginas más dedicadas a programación como [Codeacademy](http://www.codecademy.com/) han empezado a incluir Python entre sus cursos.
  * Herramientas como SAGE, Python(x,y), [WinPython](http://code.google.com/p/winpython/), Spyder, [ETS](http://code.enthought.com/projects/), ... están ahí para ayudar a que cualquiera se pueda iniciar en el cálculo científico con Python y siguen evolucionando formidablemente.
  * Python es el lenguaje más ampliamente usado en el mundo GIS pudiendo hacer cualquier cosa dentro o fuera de paquetes como arcGIS o Qgis.

**2013**

Parece que el 2013 será un buen año para Python. Aparte de los grandes paquetes, hay tantas cosas que conocer, revisar, de las que hablar, picar código, ... AYUDADNOS:

Hay muchos [scikits](http://scikits.appspot.com/scikits) pululando, incluyendo [scikit-aero](https://github.com/Juanlu001/scikit-aero), [milk](https://github.com/luispedro/milk/), [algorithms](https://github.com/nryoung/algorithms), [pyMVPA](http://www.pymvpa.org/), [PyParticles](https://github.com/simon-r/PyParticles), [Fiona](https://github.com/sgillies/fiona), [AstroML](http://astroml.github.com/), [PyCogent](http://pycogent.sourceforge.net/),  [PyMC](https://github.com/pymc-devs/pymc), [friture](https://github.com/tlecomte/friture), [PySpread](http://manns.github.com/pyspread/), [Kartograph](http://kartograph.org/),   [Chaco](http://code.enthought.com/chaco/), [PETSc](http://www.mcs.anl.gov/petsc/), [SunPy](http://www.sunpy.org/), [python-graph](http://code.google.com/p/python-graph/), [pysph](https://github.com/benma/pysph), [databrewery](http://databrewery.org/), [networkX](http://networkx.lanl.gov/), [patsy](http://patsy.readthedocs.org/en/latest/overview.html), [PyTables](http://pytables.org/), [Mayavi](http://code.enthought.com/projects/mayavi/), [Assimulo](http://www.jmodelica.org/assimulo), [Basemap](http://matplotlib.github.com/basemap/), [Biopython](http://www.biopython.org), [Blender-mathutils](http://www.blender.org/documentation/blender_python_api_2_65_release/mathutils.html), [Blist](http://pypi.python.org/pypi/blist/), [Bottleneck](http://pypi.python.org/pypi/Bottleneck), [Carray](https://github.com/FrancescAlted/carray), [CellCognition](http://www.cellcognition.org/), [CellProfiler](http://www.cellprofiler.org), [CGAL-Python](http://cgal-python.gforge.inria.fr/), [CVXOPT](http://abel.ee.ucla.edu/cvxopt/), [Delny](http://pypi.python.org/pypi/Delny), [Dipy](http://nipy.org/dipy), [Ffnet](http://ffnet.sourceforge.net/), [FiPy,](http://www.ctcms.nist.gov/fipy/) [GDAL](http://www.gdal.org/), [H5py](http://code.google.com/p/h5py/), [LibLAS](http://liblas.org/), [LIBLINEAR](http://www.csie.ntu.edu.tw/%7Ecjlin/liblinear/), [libSBML](http://sbml.org/Software/libSBML), [LIBSVM](http://www.csie.ntu.edu.tw/%7Ecjlin/libsvm/), [Libtfr](http://pypi.python.org/pypi/libtfr), [Lmfit](http://cars9.uchicago.edu/software/python/lmfit/), [MDP](http://mdp-toolkit.sourceforge.net/), [MeshPy](http://mathema.tician.de/software/meshpy), [mmLib](http://pymmlib.sourceforge.net/), [MMTK](http://dirac.cnrs-orleans.fr/MMTK), [Natgrid](http://matplotlib.sourceforge.net/users/toolkits.html#natgrid), [NetCDF4](http://code.google.com/p/netcdf4-python/), [NIPY](http://nipy.org/), [NLopt](http://ab-initio.mit.edu/nlopt), [NLTK](http://www.nltk.org/), [nMOLDYN](http://dirac.cnrs-orleans.fr/plone/software/nmoldyn/), [ODE](http://www.ode.org/), [OpenCV](http://opencv.org/), [Orange](http://orange.biolab.si/), [Polygon](http://www.j-raedler.de/projects/polygon), [PsychoPy](http://www.psychopy.org/), [PyAMG](http://code.google.com/p/pyamg/), [PyBox2D](http://code.google.com/p/pybox2d/), [PyEphem](http://rhodesmill.org/pyephem/), [PyFFTW](https://launchpad.net/pyfftw/), [PyFITS](http://www.stsci.edu/resources/software_hardware/pyfits), [pyFLTK](http://pyfltk.sourceforge.net/), [PyHDF](http://pysclint.sourceforge.net/pyhdf/), [PyMix](http://www.pymix.org), [PyMOL](http://www.pymol.org/), [Pymutt](http://code.google.com/p/pymutt/), [PyMVPA](http://www.pymvpa.org/), [Pyproj](http://code.google.com/p/pyproj/), [PySparse](http://pysparse.sourceforge.net/), [Pyspharm](http://code.google.com/p/pyspharm), [PyTST](https://github.com/nlehuen/pytst), [PyWavelets](http://pypi.python.org/pypi/PyWavelets/), [PyWCS](https://trac.assembla.com/astrolib), [QuantLib](http://quantlib.org), [Rtree](http://toblerity.github.com/rtree/), [SfePy](http://sfepy.org), [Shapely](https://github.com/sgillies/shapely), [Veusz](http://home.gna.org/veusz/), [VIGRA](http://hci.iwr.uni-heidelberg.de/vigra/), [VisionEgg](http://www.visionegg.org/), [Visvis](http://code.google.com/p/visvis/), [ViTables](http://vitables.org/), [vLFD](http://www.lfd.uci.edu/%7Egohlke/#python), [VPython](http://vpython.org/), [VTK](http://www.vtk.org), ...

**Pensamientos finales (y puntos negativos)**

Parece que el «núcleo duro» de ciencia con Python ya ha portado a Python 3, ¿y tú? Este es uno de mis primeros deberes para el 2013.

Por otra parte, siempre hemos de ser críticos para mejorar. En este sentido, la mayor crítica (autocrítica también) que encuentro es que el mundo hispano está muy poco representado, salvo honrosísimas excepciones como Fernando Pérez, Francesc Alted, Sebastian Bassi, ... Y, por lo menos en España, parece que seguimos anclados en el lapidario [¡que inventen ellos!](http://es.wikipedia.org/wiki/%C2%A1Que_inventen_ellos!) de Unamuno.

Como parte negativa de Pybonacci habría que nombrar el sesgo del blog debido a la formación de sus autores. Ninguno somos expertos en biología, finanzas, química,..., y algunos temas están mal representados. Pero eso tiene fácil solución, esperamos vuestras aportaciones 😛

Y, por mi parte, me despido hasta el año que viene. Espero que tengáis una excelente entrada en el 2013.