---
title: Trabajando con Python y R
date: 2015-06-18T19:26:25+00:00
author: Kiko Correoso
slug: trabajando-con-python-y-r
tags: cran, EVA, EVT, extremes, extremos, ipython, R, rpy2

# Trabajando de forma conjunta con Python y con R.

Hoy vamos a ver como podemos juntar lo bueno de [R](https://cran.r-project.org/), algunas de sus librerías, con Python usando **rpy2**.

Pero, lo primero de todo, ¿[qué es rpy2](https://rpy.sourceforge.net/)? rpy2 es una interfaz que permite que podamos comunicar información entre R y Python y que podamos acceder a funcionalidad de R desde Python. Por tanto, podemos estar usando Python para todo nuestro análisis y en el caso de que necesitemos alguna librería estadística especializada de R podremos acceder a la misma usando rpy2.

Para poder usar rpy2 necesitarás tener [instalado tanto Python (CPython versión >= 2.7.x) como R (versión >=3)](https://rpy.sourceforge.net/rpy2/doc-2.5/html/overview.html#requirements), además de las librerías R a las que quieras acceder. [Conda permite realizar todo el proceso de instalación de los intérpretes de Python y R, además de librerías](https://continuum.io/conda-for-R), pero no he trabajado con Conda y R por lo que no puedo aportar mucho más en este aspecto. Supongo que será parecido a lo que hacemos con Conda y Python.

Para este microtutorial voy a hacer uso de la librería **[extRemes](https://cran.r-project.org/web/packages/extRemes/index.html)** de R que permite hacer análisis de valores extremos usando varias de las metodologías más comúnmente aceptadas.

Como siempre, primero de todo, importaremos la funcionalidad que necesitamos para la ocasión.

    :::python
    # Importamos pandas y numpy para manejar los datos que pasaremos a R
    import pandas as pd
    import numpy as np

    # Usamos rpy2 para interactuar con R
    import rpy2.robjects as ro

    # Activamos la conversión automática de tipos de rpy2
    import rpy2.robjects.numpy2ri
    rpy2.robjects.numpy2ri.activate()

    import matplotlib.pyplot as plt
    %matplotlib inline

En el anterior código podemos ver una serie de cosas nuevas que voy a explicar brevemente:

*  `import rpy2.robjects as ro`, esto lo explicaremos un poquito más abajo.
*  `import rpy2.robjects.numpy2ri`, importamos el módulo numpy2ri. Este módulo permite que hagamos conversión automática de objetos numpy a objetos rpy2.
*  `rpy2.robjects.numpy2ri.activate()`, hacemos uso de la función `activate` que activa la conversión automática de objetos que hemos comentado en la línea anterior.

# Brevísima introducción a algunas de las cosas más importantes de rpy2.

Para evaluar directamente código R podemos hacerlo usando `rpy2.robjects.r` con el código R expresado como una cadena (`rpy2.robjects` lo he importado como `ro` en este caso, como podéis ver más arriba):

    :::
    codigo_r = """
    saluda <- function(cadena) {
     return(paste("Hola, ", cadena))
    }
    """
    ro.r(codigo_r)

**OUTPUT:**

`<SignatureTranslatedFunction - Python:0x03096490 / R:0x03723E98>`

En la anterior celda hemos creado una función R llamada `saluda` y que ahora está disponible en el espacio de nombres global de R. Podemos acceder a la misma desde Python de la siguiente forma:

`saluda_py = ro.globalenv['saluda']`

Y podemos usarla de la siguiente forma:

    :::python
    res = saluda_py('pepe')
    print(res[])

**OUTPUT:**

`Hola,  pepe`

En la anterior celda véis que para acceder al resultado he tenido que usar `res[0]`. En realidad, lo que nos devuleve rpy2 es:

    :::python
    print(type(res))
    print(res.shape)

**OUTPUT:**

    <class ';numpy.ndarray';>
    (1,)

En este caso un numpy array con diversa información del objeto rpy2. Como el objeto solo devuelve un string pues el numpy array solo tiene un elemento.

Podemos acceder al código R de la función de la siguiente forma:

`print(saluda_py.r_repr())`

**OUTPUT:**

    function (cadena) 
    {
        return(paste("Hola, ", cadena))
    }

Hemos visto como acceder desde Python a nombres disponibles en el entorno global de R. ¿Cómo podemos hacer para que algo que creemos en Python este accesible en R?

`variable_r_creada_desde_python = ro.FloatVector(np.arange(1,5,0.1))`

Veamos como es esta `variable_r_creada_desde_python` dentro de Python

`variable_r_creada_desde_python`

**OUTPUT:**

    <FloatVector - Python:0x09D5A7B0 / R:0x07FE8900>
    [1.000000, 1.100000, 1.200000, ..., 4.700000, 4.800000, 4.900000]

¿Y lo que se tendría que ver en R?

`print(variable_r_creada_desde_python.r_repr())`

**OUTPUT:**

    c(1, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2, 2.1, 2.2, 
    2.3, 2.4, 2.5, 2.6, 2.7, 2.8, 2.9, 3, 3.1, 3.2, 3.3, 3.4, 3.5, 
    3.6, 3.7, 3.8, 3.9, 4, 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7, 4.8, 
    4.9)

Pero ahora mismo esa variable no está disponible desde R y no la podríamos usar dentro de código R que permanece en el espacio R (vaya lío, ¿no?)

`ro.r('variable_r_creada_desde_python')`

**OUTPUT:**

    ---------------------------------------------------------------------------
    RRuntimeError                             Traceback (most recent call last)
    <ipython-input-10-524753a78365> in <module>()
    ----> 1  ro.r(';variable_r_creada_desde_python';)
    d:\users\X003621\AppData\Local\Continuum\Miniconda3\lib\site-packages\rpy2\robjects\_\_init__.py in __call__(self, string)
     251     def __call__(self, string):
     252         p = rinterface.parse(string)
    --> 253  res = self.eval(p)
     254         return res
     255 

    d:\users\X003621\AppData\Local\Continuum\Miniconda3\lib\site-packages\rpy2\robjects\functions.py in __call__(self, *args, **kwargs)
     168                 v = kwargs.pop(k)
     169                 kwargs[r_k] = v
    --> 170  return super(SignatureTranslatedFunction, self).__call__(*args, **kwargs)
     171 
     172 pattern_link = re.compile(r';\\link\{(.+?)\}';)

    d:\users\X003621\AppData\Local\Continuum\Miniconda3\lib\site-packages\rpy2\robjects\functions.py in __call__(self, *args, **kwargs)
     98         for k, v in kwargs.items():
     99             new_kwargs[k] = conversion.py2ri(v)
    --> 100  res = super(Function, self).__call__(*new_args, **new_kwargs)
     101         res = conversion.ri2ro(res)
     102         return res

    RRuntimeError: Error in eval(expr, envir, enclos) : 
      object ';variable_r_creada_desde_python'; not found

Vale, tendremos que hacer que sea accesible desde R de la siguiente forma:

    ro.globalenv["variable_ahora_en_r"] = variable_r_creada_desde_python
    print(ro.r("variable_ahora_en_r"))

**OUTPUT:**

    [ 1.   1.1  1.2  1.3  1.4  1.5  1.6  1.7  1.8  1.9  2.   2.1  2.2  2.3  2.4
      2.5  2.6  2.7  2.8  2.9  3.   3.1  3.2  3.3  3.4  3.5  3.6  3.7  3.8  3.9
      4.   4.1  4.2  4.3  4.4  4.5  4.6  4.7  4.8  4.9]

Ahora que ya la tenemos accesible la podemos usar desde R. Por ejemplo, vamos a usar la función `sum` en R que suma los elementos pero directamente desde R:

    print(ro.r('sum(variable_ahora_en_r)'))
    print(np.sum(variable_r_creada_desde_python))

**OUTPUT:**

    [ 118.]
    118.0

Perfecto, ya sabemos, de forma muy sencilla y básica, como podemos usar R desde Python, como podemos pasar información desde R hacia Python y desde Python hacia R. ¡¡¡Esto es muy poderoso!!!, estamos juntando lo mejor de dos mundos, la solidez de las herramientas científicas de Python con la funcionalidad especializada que nos pueden aportar algunas librerías de R no disponibles en otros ámbitos.

Trabajando de forma híbrida entre Python y R

Vamos a empezar importando la librería _extRemes_ de R:

    # Importamos la librería extRemes de R
    from rpy2.robjects.packages import importr
    extremes = importr('extRemes')

En la anterior celda hemos hecho lo siguiente:

*  `from rpy2.robjects.packages import importr`, La función `importr` nos servirá para importar las librerías R
*  `extremes = importr('extRemes')`, de esta forma importamos la librería `extRemes` de R, sería equivalente a hacer en R `library(extRemes)`.

Leemos datos con pandas. En el mismo repo donde está este notebook está también un fichero de texto con datos que creé a priori. Supuestamente son datos horarios de velocidad del viento por lo que vamos a hacer análisis de valores extremos de velocidad del viento horaria.

    data = pd.read_csv('datasets/Synthetic_data.txt',
                       sep = '\s*', skiprows = 1, parse_dates = [[, 1]],
                       names = ['date','time','wspd'], index_col = )

    data.head(3)

<div>
  <div style="max-height:1000px;max-width:1500px;overflow:auto;">
    <table border="1" class="dataframe">
      <tr style="text-align: right;">
        <th>
        </th>
        
        <th>
          wspd
        </th>
      </tr>
      
      <tr>
        <th>
          date_time
        </th>
        
        <th>
        </th>
      </tr>
      
      <tr>
        <th>
          1983-01-01 00:00:00
        </th>
        
        <td>
          7.9
        </td>
      </tr>
      
      <tr>
        <th>
          1983-01-01 01:00:00
        </th>
        
        <td>
          8.2
        </td>
      </tr>
      
      <tr>
        <th>
          1983-01-01 02:00:00
        </th>
        
        <td>
          8.5
        </td>
      </tr>
    </table>
  </div>
</div>

Extraemos los máximos anuales los cuales usaremos posteriormente dentro de R para hacer cálculo de valores extremos usando la [distribución generalizada de valores extremos (GEV)](httpss://en.wikipedia.org/wiki/Generalized_extreme_value_distribution):

`max_y = data.wspd.groupby(pd.TimeGrouper(freq = 'A')).max()`

Dibujamos los valores máximos anuales usando Pandas:

`max_y.plot(kind = 'bar', figsize = (12, 4))`

**OUTPUT:**

`<matplotlib.axes._subplots.AxesSubplot at 0x10a923d0>`

![](https://pybonacci.org/images/2015/06/wpid-Trabajando_con_Python_y_R1.png?style=centerme)

Referenciamos la funcionalidad [`fevd` (_fit extreme value distribution_) dentro del paquete `extremes`](https://cran.r-project.org/web/packages/extRemes/extRemes.pdf) de R para poder usarla directamente con los valores máximos que hemos obtenido usando Pandas y desde Python.

`fevd = extremes.fevd`   

Como hemos comentado anteriormente, vamos a calcular los parámetros de la GEV usando el método de ajuste `GMLE` (_Generalised Maximum Lihelihood Estimation_) y los vamos a guardar directamente en una variable Python.

Veamos la ayuda antes:

p`rint(fevd.__doc__)`

    Python representation of an R function.
    description
    -----------


     Fit a univariate extreme value distribution functions (e.g., GEV, GP, PP, Gumbel, or Exponential) to data; possibly with covariates in the parameters.
     


    fevd(
        x,
        data,
        threshold = rinterface.NULL,
        threshold_fun = ~,
        location_fun = ~,
        scale_fun = ~,
        shape_fun = ~,
        use_phi = False,
        type = c,
        method = c,
        initial = rinterface.NULL,
        span,
        units = rinterface.NULL,
        time_units = days,
        period_basis = year,
        na_action = <rpy2.rinterface.SexpVector - Python:0x116D6C50 / R:0x0C4BB100>,
        optim_args = rinterface.NULL,
        priorFun = rinterface.NULL,
        priorParams = rinterface.NULL,
        proposalFun = rinterface.NULL,
        proposalParams = rinterface.NULL,
        iter = 9999.0,
        weights = 1.0,
        blocks = rinterface.NULL,
        verbose = False,
    )

    x :  `fevd`: `x` can be a numeric vector, the name of a column of `data` or a formula giving the data to which the EVD is to be fit.  In the case of the latter two, the `data` argument must be specified, and must have appropriately named columns.`plot` and `print` method functions: any list object returned by `fevd`. ,

    object :  A list object of class \dQuote{fevd} as returned by `fevd`. ,

    data :  A data frame object with named columns giving the data to be fit, as well as any data necessary for modeling non-stationarity through the threshold and/or any of the parameters. ,

    threshold :  numeric (single or vector).  If fitting a peak over threshold (POT) model (i.e., `type` = \dQuote{PP}, \dQuote{GP}, \dQuote{Exponential}) this is the threshold over which (non-inclusive) data (or excesses) are used to estimate the parameters of the distribution function.  If the length is greater than 1, then the length must be equal to either the length of `x` (or number of rows of `data`) or to the number of unique arguments in `threshold.fun`. ,

    threshold.fun :  formula describing a model for the thresholds using columns from `data`.  Any valid formula will work.  `data` must be supplied if this argument is anything other than ~ 1.  Not for use with `method` \dQuote{Lmoments}. ,

    location.fun :  formula describing a model for each parameter using columns from `data`.  `data` must be supplied if any of these arguments are anything other than ~ 1. ,

    scale.fun :  formula describing a model for each parameter using columns from `data`.  `data` must be supplied if any of these arguments are anything other than ~ 1. ,

    shape.fun :  formula describing a model for each parameter using columns from `data`.  `data` must be supplied if any of these arguments are anything other than ~ 1. ,

    use.phi :  logical; should the log of the scale parameter be used in the numerical optimization (for `method` \dQuote{MLE}, \dQuote{GMLE} and \dQuote{Bayesian} only)?  For the ML and GML estimation, this may make things more stable for some data. ,

    type :  `fevd`: character stating which EVD to fit.  Default is to fit the generalized extreme value (GEV) distribution function (df).`plot` method function: character describing which plot(s) is (are) desired.  Default is \dQuote{primary}, which makes a 2 by 2 panel of plots including the QQ plot of the data quantiles against the fitted model quantiles (`type` \dQuote{qq}), a QQ plot (\dQuote{qq2}) of quantiles from model-simulated data against the data, a density plot of the data along with the model fitted density (`type` \dQuote{density}) and a return level plot (`type` \dQuote{rl}). In the case of a stationary (fixed) model, the return level plot will show return levels calculated for return periods given by `return.period`, along with associated CIs (calculated using default `method` arguments depending on the estimation method used in the fit.  For non-stationary models, the data are plotted as a line along with associated effective return levels for return periods of 2, 20 and 100 years (unless `return.period` is specified by the user to other values.  Other possible values for `type` include \dQuote{hist}, which is similar to \dQuote{density}, but shows the histogram for the data and \dQuote{trace}, which is not used for L-moment fits.  In the case of MLE/GMLE, the trace yields a panel of plots that show the negative log-likelihood and gradient negative log-likelihood (note that the MLE gradient is currently used even for GMLE) for each of the estimated parameter(s); allowing one parameter to vary according to `prange`, while the others remain fixed at their estimated values.  In the case of Bayesian estimation, the \dQuote{trace} option creates a panel of plots showing the posterior df and MCMC trace for each parameter. ,

    method :  `fevd`: character naming which type of estimation method to use.  Default is to use maximum likelihood estimation (MLE). ,

    initial :  A list object with any named parameter component giving the initial value estimates for starting the numerical optimization (MLE/GMLE) or the MCMC iterations (Bayesian).  In the case of MLE/GMLE, it is best to obtain a good intial guess, and in the Bayesian case, it is perhaps better to choose poor initial estimates.  If NULL (default), then L-moments estimates and estimates based on Gumbel moments will be calculated, and whichever yields the lowest negative log-likelihood is used.  In the case of `type` \dQuote{PP}, an additional MLE/GMLE estimate is made for the generalized Pareto (GP) df, and parameters are converted to those of the Poisson Process (PP) model.  Again, the initial estimates yielding the lowest negative log-likelihoo value are used for the initial guess. ,

    span :  single numeric giving the number of years (or other desired temporal unit) in the data set.  Only used for POT models, and only important in the estimation for the PP model, but important for subsequent estimates of return levels for any POT model.  If missing, it will be calculated using information from `time.units`. ,

    units :  (optional) character giving the units of the data, which if given may be used subsequently (e.g., on plot axis labels, etc.). ,

    time.units :  character string that must be one of \dQuote{hours}, \dQuote{minutes}, \dQuote{seconds}, \dQuote{days}, \dQuote{months}, \dQuote{years}, \dQuote{m/hour}, \dQuote{m/minute}, \dQuote{m/second}, \dQuote{m/day}, \dQuote{m/month}, or \dQuote{m/year}; where m is a number.  If `span` is missing, then this argument is used in determining the value of `span`.  It is also returned with the output and used subsequently for plot labelling, etc. ,

    period.basis :  character string giving the units for the period.  Used only for plot labelling and naming output vectors from some of the method functions (e.g., for establishing what the period represents for the return period). ,

    rperiods :  numeric vector giving the return period(s) for which it is desired to calculate the corresponding return levels. ,

    period :  character string naming the units for the return period. ,

    burn.in :  The first `burn.in` values are thrown out before calculating anything from the MCMC sample. ,

    a :  when plotting empirical probabilies and such, the function `ppoints` is called, which has this argument `a`. ,

    d :  numeric determining how to scale the rate parameter for the point process.  If NULL, the function will attempt to scale based on the values of `period.basis` and `time.units`, the first of which must be \dQuote{year} and the second of which must be one of \dQuote{days}, \dQuote{months}, \dQuote{years}, \dQuote{hours}, \dQuote{minutes} or \dQuote{seconds}.  If none of these are the case, then `d` should be specified, otherwise, it is not necessary. ,

    density.args :  named list object containing arguments to the `density` and `hist` functions, respectively. ,

    hist.args :  named list object containing arguments to the `density` and `hist` functions, respectively. ,

    na.action :  function to be called to handle missing values.  Generally, this should remain at the default (na.fail), and the user should take care to impute missing values in an appropriate manner as it may have serious consequences on the results. ,

    optim.args :  A list with named components matching exactly any arguments that the user wishes to specify to `optim`, which is used only for MLE and GMLE methods.  By default, the \dQuote{BFGS} method is used along with `grlevd` for the gradient argument.  Generally, the `grlevd` function is used for the `gr` option unless the user specifies otherwise, or the optimization method does not take gradient information. ,

    priorFun :  character naming a prior df to use for methods GMLE and Bayesian.  The default for GMLE (not including Gumbel or Exponential types) is to use the one suggested by Martins and Stedinger (2000, 2001) on the shape parameter; a beta df on -0.5 to 0.5 with parameters `p` and `q`.  Must take `x` as its first argument for `method` \dQuote{GMLE}.  Optional arguments for the default function are `p` and `q` (see details section).The default for Bayesian estimation is to use normal distribution functions.  For Bayesian estimation, this function must take `theta` as its first argument.Note: if this argument is not NULL and `method` is set to \dQuote{MLE}, it will be changed to \dQuote{GMLE}. ,

    priorParams :  named list containing any prior df parameters (where the list names are the same as the function argument names).  Default for GMLE (assuming the default function is used) is to use `q` = 6 and `p` = 9.  Note that in the Martins and Stedinger (2000, 2001) papers, they use a different EVD parametrization than is used here such that a positive shape parameter gives the upper bounded distribution instead of the heavy-tail one (as emloyed here).  To be consistent with these papers, `p` and `q` are reversed inside the code so that they have the same interpretation as in the papers.Default for Bayesian estimation is to use ML estimates for the means of each parameter (may be changed using `m`, which must be a vector of same length as the number of parameters to be estimated (i.e., if using the default prior df)) and a standard deviation of 10 for all other parameters (again, if using the default prior df, may be changed using `v`, which must be a vector of length equal to the number of parameters). ,

    proposalFun :  For Bayesian estimation only, this is a character naming a function used to generate proposal parameters at each iteration of the MCMC.  If NULL (default), a random walk chain is used whereby if theta.i is the current value of the parameter, the proposed new parameter theta.star is given by theta.i + z, where z is drawn at random from a normal df. ,

    proposalParams :  A named list object describing any optional arguments to the `proposalFun` function.  All functions must take argument `p`, which must be a vector of the parameters, and `ind`, which is used to identify which parameter is to be proposed.  The default `proposalFun` function takes additional arguments `mean` and `sd`, which must be vectors of length equal to the number of parameters in the model (default is to use zero for the mean of z for every parameter and 0.1 for its standard deviation). ,

    iter :  Used only for Bayesian estimation, this is the number of MCMC iterations to do. ,

    weights :  numeric of length 1 or n giving weights to be applied     in the likelihood calculations (e.g., if there are data points to     be weighted more/less heavily than others). ,

    blocks :  An optional list containing information required to fit point process models in a computationally-efficient manner by using only the exceedances and not the observations below the threshold(s). See details for further information.       ,

    FUN :  character string naming a function to use to estimate the parameters from the MCMC sample.  The function is applied to each column of the `results` component of the returned `fevd` object. ,

    verbose :  logical; should progress information be printed to the screen?  If TRUE, for MLE/GMLE, the argument `trace` will be set to 6 in the call to `optim`. ,

    prange :  matrix whose columns are numeric vectors of length two for each parameter in the model giving the parameter range over which trace plots should be made.  Default is to use either +/- 2 * std. err. of the parameter (first choice) or, if the standard error cannot be calculated, then +/- 2 * log2(abs(parameter)).  Typically, these values seem to work very well for these plots. ,

    ... :  Not used by most functions here.  Optional arguments to `plot` for the various `plot` method functions.In the case of the `summary` method functions, the logical argument `silent` may be passed to suppress (if TRUE) printing any information to the screen. ,

Y ahora vamos a hacer un cálculo sin meternos mucho en todas las opciones posibles.

`res = fevd(max_y.values, type = "GEV", method = "GMLE")`

¿Qué estructura tiene la variable `res` que acabamos de crear y que tiene los resultados del ajuste?

`print(type(res))`

**OUTPUT:**

`<class ';rpy2.robjects.vectors.ListVector';>`

`print(res.r_repr)`

**OUTPUT:**

    <bound method ListVector.r_repr of <ListVector - Python:0x10AB8878 / R:0x0CA9B458>
    [Vector, ndarray, ndarray, ..., ndarray, ListV..., ListV...]
      call: <class ';rpy2.robjects.vectors.Vector';>
      <Vector - Python:0x10AB8418 / R:0x0CB2FFB4>
    [RNULLType, Vector, Vector, Vector]
      data.name: <class ';numpy.ndarray';>
      array([';structure(c(22.2, 25.5, 21.5, 22.5, 23.7, 22.5, 21.7, 29.7, 24.2, ';,
           ';23.8, 28.1, 23.4, 23.7, 25.6, 23.2, 24.9, 22.8, 24.6, 22.3, 25.5, ';,
           ';22.6, 24, 20.8, 23.5, 24.4, 24.1, 25.1, 19.4, 22.8, 24.2, 25, ';,
           ';25.3), .Dim = 32L)';, ';';], 
          dtype=';<U66';)
      weights: <class ';numpy.ndarray';>
      array([ 1.])
      ...
      call: <class ';numpy.ndarray';>
      array([';location';, ';scale';, ';shape';], 
          dtype=';<U8';)
    <ListVector - Python:0x10AB8878 / R:0x0CA9B458>
    [Vector, ndarray, ndarray, ..., ndarray, ListV..., ListV...]
    <ListVector - Python:0x10AB8878 / R:0x0CA9B458>
    [Vector, ndarray, ndarray, ..., ndarray, ListV..., ListV...]>

Según nos indica lo anterior, ahora `res` es un vector que está compuesto de diferentes elementos. Los vectores pueden tener un nombre para todos o algunos de los elementos. Para acceder a estor nombres podemos hacer:

`res.names`

**OUTPUT:**

    array([';call';, ';data.name';, ';weights';, ';in.data';, ';x';, ';priorFun';,
           ';priorParams';, ';method';, ';type';, ';period.basis';, ';par.models';,
           ';const.loc';, ';const.scale';, ';const.shape';, ';n';, ';na.action';,
           ';parnames';, ';results';, ';initial.results';], 
          dtype=';<U15';)

Según el output anterior, parece que hay un nombre `results`, ahí es donde se guardan los valores del ajuste, los estimadores. Para acceder al mismo podemos hacerlo de diferentes formas. Con Python tendriamos que saber el índice y acceder de forma normal (`__getitem__()`). Existe una forma alternativa usando el método `rx` que nos permite acceder directamente con el nombre:

    results = res.rx('results')
    print(results.r_repr)

**OUTPUT:**

    <bound method ListVector.r_repr of <ListVector - Python:0x10ABBCB0 / R:0x0CBFBC40>
    [ListVector]
    <ListVector - Python:0x10ABBCB0 / R:0x0CBFBC40>
    [ListVector]>

Parece que tenemos un único elemento:

    results = results[]
    results.r_repr

**OUTPUT:**

    <bound method ListVector.r_repr of <ListVector - Python:0x10ABF490 / R:0x0C851BA0>
    [ndarray, ndarray, ndarray, ..., RNULL..., ndarray, ListV...]
      par: <class ';numpy.ndarray';>
      array([ 23.06394152,   1.75769129,  -0.16288164])
      value: <class ';numpy.ndarray';>
      array([  1.00000000e+16])
      counts: <class ';numpy.ndarray';>
      array([1, 1], dtype=int32)
      ...
      par: <class ';rpy2.rinterface.RNULLType';>
      rpy2.rinterface.NULL
      value: <class ';numpy.ndarray';>
      array([[ 0.,  0.,  0.],
           [ 0.,  0.,  0.],
           [ 0.,  0.,  0.]])
    <ListVector - Python:0x10ABF490 / R:0x0C851BA0>
    [ndarray, ndarray, ndarray, ..., RNULL..., ndarray, ListV...]>

Vemos ahora que `results` tiene un elemento con nombre `par` donde se guardan los valores de los estimadores del ajuste a la GEV que hemos obtenido usando GMLE. Vamos a obtener finalmente los valores de los estimadores:

    location, scale, shape = results.rx('par')[][:]
    print(location, scale, shape)

**OUTPUT:**

`23.0639415199 1.75769128743 -0.162881636772`

# Funcion mágica para R (antigua `rmagic`)

Usamos la antigua función mágica `rmagic` que ahora se activará en el notebook de la siguiente forma:

`%load_ext rpy2.ipython`

Veamos como funciona la functión mágica de R:

`help(rpy2.ipython.rmagic.RMagics.R)`

**OUTPUT:**

    Help on function R in module rpy2.ipython.rmagic:

    R(self, line, cell=None, local_ns=None)
        ::
        
          %R [-i INPUT] [-o OUTPUT] [-n] [-w WIDTH] [-h HEIGHT] [-p POINTSIZE]
                 [-b BG] [--noisolation] [-u {px,in,cm,mm}] [-r RES]
                 
        Execute code in R, optionally returning results to the Python runtime.
        
        In line mode, this will evaluate an expression and convert the returned
        value to a Python object.  The return value is determined by rpy2';s
        behaviour of returning the result of evaluating the final expression.
        
        Multiple R expressions can be executed by joining them with semicolons::
        
            In [9]: %R X=c(1,4,5,7); sd(X); mean(X)
            Out[9]: array([ 4.25])
        
        In cell mode, this will run a block of R code. The resulting value
        is printed if it would printed be when evaluating the same code
        within a standard R REPL.
        
        Nothing is returned to python by default in cell mode::
        
            In [10]: %%R
               ....: Y = c(2,4,3,9)
               ....: summary(lm(Y~X))
        
            Call:
            lm(formula = Y ~ X)
        
            Residuals:
                1     2     3     4
             0.88 -0.24 -2.28  1.64
        
            Coefficients:
                        Estimate Std. Error t value Pr(>|t|)
            (Intercept)   0.0800     2.3000   0.035    0.975
            X             1.0400     0.4822   2.157    0.164
        
            Residual standard error: 2.088 on 2 degrees of freedom
            Multiple R-squared: 0.6993,Adjusted R-squared: 0.549
            F-statistic: 4.651 on 1 and 2 DF,  p-value: 0.1638
        
        In the notebook, plots are published as the output of the cell::
        
            %R plot(X, Y)
        
        will create a scatter plot of X bs Y.
        
        If cell is not None and line has some R code, it is prepended to
        the R code in cell.
        
        Objects can be passed back and forth between rpy2 and python via the -i -o flags in line::
        
            In [14]: Z = np.array([1,4,5,10])
        
            In [15]: %R -i Z mean(Z)
            Out[15]: array([ 5.])
        
            In [16]: %R -o W W=Z*mean(Z)
            Out[16]: array([  5.,  20.,  25.,  50.])
        
            In [17]: W
            Out[17]: array([  5.,  20.,  25.,  50.])
        
        The return value is determined by these rules:
        
        * If the cell is not None (i.e., has contents), the magic returns None.
        
        * If the final line results in a NULL value when evaluated
          by rpy2, then None is returned.
        
        * No attempt is made to convert the final value to a structured array.
          Use %Rget to push a structured array.
        
        * If the -n flag is present, there is no return value.
        
        * A trailing ';;'; will also result in no return value as the last
          value in the line is an empty string.
        
        optional arguments:
          -i INPUT, --input INPUT
                                Names of input variable from shell.user_ns to be
                                assigned to R variables of the same names after
                                calling self.pyconverter. Multiple names can be passed
                                separated only by commas with no whitespace.
          -o OUTPUT, --output OUTPUT
                                Names of variables to be pushed from rpy2 to
                                shell.user_ns after executing cell body (rpy2';s
                                internal facilities will apply ri2ro as appropriate).
                                Multiple names can be passed separated only by commas
                                with no whitespace.
          -n, --noreturn        Force the magic to not return anything.
        
        Plot:
          Arguments to plotting device
        
          -w WIDTH, --width WIDTH
                                Width of plotting device in R.
          -h HEIGHT, --height HEIGHT
                                Height of plotting device in R.
          -p POINTSIZE, --pointsize POINTSIZE
                                Pointsize of plotting device in R.
          -b BG, --bg BG        Background of plotting device in R.
        
        SVG:
          SVG specific arguments
        
          --noisolation         Disable SVG isolation in the Notebook. By default,
                                SVGs are isolated to avoid namespace collisions
                                between figures.Disabling SVG isolation allows to
                                reference previous figures or share CSS rules across a
                                set of SVGs.
        
        PNG:
          PNG specific arguments
        
          -u <{px,in,cm,mm}>, --units <{px,in,cm,mm}>
                                Units of png plotting device sent as an argument to
                                *png* in R. One of ["px", "in", "cm", "mm"].
          -r RES, --res RES     Resolution of png plotting device sent as an argument
                                to *png* in R. Defaults to 72 if *units* is one of
                                ["in", "cm", "mm"].
          code

A veces, será más simple usar la función mágica para interactuar con R. Veamos un ejemplo donde le pasamos a R el valor obtenido de la función `fevd` del paquete `extRemes` de R que he usado anteriormente y corremos cierto código directamente desde R sin tener que usar `ro.r`.

`%R -i res plot.fevd(res)`

![](https://pybonacci.org/images/2015/06/wpid-Trabajando_con_Python_y_R2.png?style=centerme)

En la anterior celda de código le he pasado como parámetro de entrada (`- i res`) la variable `res` que había obtenido anteriormente para que esté disponible desde R. y he ejecutado código R puro (`plot.fevd(res)`).

Si lo anterior lo quiero hacer con rpy2 puedo hacer lo siquiente:

CUIDADO, la siguiente celda de código puede provocar que se reinicialice el notebook y se rompa la sesión. Si has hecho cambios en el notebook guárdalos antes de ejecutar la celda, por lo que pueda pasar...

    ro.globalenv['res'] = res
    ro.r("plot.fevd(res)")

    rpy2.rinterface.NULL

Lo anterior me bloquea el notebook y me 'rompe' la sesión ([en windows, al menos](httpss://bitbucket.org/rpy2/rpy2/issues?q=windows)) ya que la ventana de gráficos se abre de forma externa... Por tanto, una buena opción para trabajar de forma interactiva con Python y R de forma conjunta y que no se 'rompa' nada es usar tanto rpy2 como su extensión para el notebook de Jupyter (dejaremos de llamarlo IPython poco a poco).

# Usando Python y R combinando rpy2 y la función mágica

Vamos a combinar las dos formas de trabajar con rpy2 en el siguiente ejemplo:

    metodos = ["MLE", "GMLE"]
    tipos = ["GEV", "Gumbel"]

Lo que vamos a hacer es calcular los parámetros del ajuste usando la distribución GEV y Gumbel, que es un caso especial de la GEV. El ajuste lo calculamos usando tanto MLE como GMLE. Además de mostrar los valores resultantes del ajuste para los estimadores vamos a mostrar el dibujo de cada uno de los ajustes y algunos test de bondad. Usamos Python para toda la maquinaria de los bucles, usamos rpy2 para obtener los estimadores y usamos la función mágica de rpy2 para mostrar los gráficos del resultado.

    :::python
    for t in tipos:
        for m in metodos:
            print('tipo de ajuste: ', t)
            print('método de ajuste: ', m)
            res = fevd(max_y.values, method = m, type = t)
            if m == "Bayesian":
                print(res.rx('results')[][-1][:-2])
            elif m == "Lmoments":
                print(res.rx('results')[])
            else:
                print(res.rx('results')[].rx('par')[][:])
            %R -i res plot.fevd(res)

**OUTPUT:**

    tipo de ajuste:  GEV
    método de ajuste:  MLE
    [ 23.05170779   1.80858528  -0.14979836]

![](https://pybonacci.org/images/2015/06/wpid-Trabajando_con_Python_y_R3.png?style=centerme)

    tipo de ajuste:  GEV
    método de ajuste:  GMLE
    [ 23.06394152   1.75769129  -0.16288164]

![](https://pybonacci.org/images/2015/06/wpid-Trabajando_con_Python_y_R4.png?style=centerme)

    tipo de ajuste:  Gumbel
    método de ajuste:  MLE
    [ 22.90587606   1.81445179]

![](https://pybonacci.org/images/2015/06/wpid-Trabajando_con_Python_y_R5.png?style=centerme)

    tipo de ajuste:  Gumbel
    método de ajuste:  GMLE
    [ 22.90587606   1.81445179]

![](https://pybonacci.org/images/2015/06/wpid-Trabajando_con_Python_y_R6.png?style=centerme)

# Comentarios finales

Espero que este microtutorial os valga, al menos, para conocer rpy2 y la potencia que os puede llegar a aportar a vuestros análisis 'pythónicos'. Como resumen:

*  Tenemos en nuestras manos una herramienta muy poderosa.
*  Rpy2 puede estar poco madura en algún aspecto aunque ha mejorado bastante con respecto a alguna versión de rpy2 que usé anteriormente.
*  También podéis usar directamente [R como kernel](httpss://github.com/IRkernel/IRkernel), aunque perdéis la interacción con Python. También puede ocurrir que la instalación os haga perder mucho el tiempo [para poder hacerlo funcionar](httpss://github.com/IRkernel/IRkernel/issues/54) si os veis obligados a usarlo desde windows.
*  En la elaboración de este microtutorial la consola de R donde iba haciendo algunas pruebas simples se me ha 'roto' muchísimas más veces de las que consideraría aceptables. No se puede quedar colgada, cerrar,..., seis o siete veces en media hora una consola haciendo cosas simples. Eso hace que si quieres usar R de forma interactiva debas usar alternativas como Jupyter, RStudio u otros que desconozco ya que la consola oficial no está 'ni pa pipas' (por lo menos en Windows, el sistema operativo con más usuarios potenciales, mal que me pese).
*  Sigo manteniendo muchas reservas respecto a R como Lenguaje de Programación (en mayúsculas) por lo que si puedo limitar su uso a alguna librería especializada que necesito y a la que pueda acceder con rpy2 es lo que seguiré haciendo (_[If you are using R and you think you're in hell, this is a map for you](https://www.burns-stat.com/pages/Tutor/R_inferno.pdf)._)

# Y el notebook...

En el caso de que queráis trastear con el notebook lo podéis descargar desde [aquí](https://nbviewer.ipython.org/github/Pybonacci/notebooks/tree/master/Trabajando_con_R_Python/). También podéis [descargar todos los notebooks desde nuestro repo oficial de notebooks](httpss://github.com/Pybonacci/notebooks).
