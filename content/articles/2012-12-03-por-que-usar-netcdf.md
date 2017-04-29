---
title: ¿Por qué usar netCDF?
date: 2012-12-03T08:43:37+00:00
author: Kiko Correoso
slug: por-que-usar-netcdf
tags: array-oriented, arrays, hdf, hdf5, netcdf, netcdf-4, netcdf4-python

Primero de todo empezaremos por el principio

**¿Qué es [netCDF](http://en.wikipedia.org/wiki/NetCDF)?**

Es un conjunto de librerías (o bibliotecas) y un formato de datos que son:

  *  **auto-descriptivo** ya que incluye información acerca de los datos contenidos en el fichero netCDF
  * **_independiente de la plataforma_**
  * podemos **_acceder_** a un subconjunto de datos del fichero **de forma eficiente**
  * permite **_agregar_ datos** a un fichero ya existente sin necesidad de copiar los datos ya existentes en el fichero
  * puede ser **fácilmente _compartido_** ya que una persona puede escribir mientras varias personas pueden leer el mismo fichero.
  * puede ser **_archivado_** ya que las versiones previas siempre estarán soportadas por las nuevas versiones

Su actual versión es la 4 y permite leer los ficheros creados con versiones anteriores de netCDF, como se ha comentado anteriormente.

[Además es compatible con un subconjunto de HDF5](http://www.unidata.ucar.edu/software/netcdf/docs/interoperability_hdf5.html) (del que hablaremos otro día, Francesc, ¿te animas como firma invitada?) pudiendo leer gran cantidad de ficheros en formato HDF5 pero no todos. HDF5 es capaz de abrir cualquier fichero creado con netCDF-4 (que es el modelo mejorado de datos que veremos a continuación). Es decir, un fichero netCDF-4 es un fichero HDF5 pero no a la inversa.

Es además un estándar para varias [instituciones](http://www.unidata.ucar.edu/software/netcdf/docs/standards.html) como la [Open Geospatial Consortium](http://www.opengeospatial.org/standards/netcdf).

**¿Cuál es el formato de un fichero netCDF?**

El formato no es único, existe un modelo clásico, más sencillo, y el modelo mejorado (llamado netCDF4), más complejo y completo.

<!--more-->

El [modelo clásico](http://www.unidata.ucar.edu/software/netcdf/workshops/2008/datamodel/NcClassicModel.html) consta de un cabecero, que contiene toda la información sobre las dimensiones, atributos y nombres de las variables contenidas y la parte de los datos, comprendiendo los datos de las variables de tamaño fijo, y los datos de tamaño variable, conteniendo los datos de las variables que tienen dimensión ilimitada.

El [modelo mejorado](http://www.unidata.ucar.edu/software/netcdf/workshops/2008/netcdf4/Nc4DataModel.html) (netCDF-4) permite estructuras más complejas de datos con tipos de datos definidos por el usuario, permitiendo almacenarlos de forma jerárquica mediante grupos (que serían como carpetas en un sistema de ficheros),...

**Acceso a ficheros**

Se puede acceder a ficheros en disco, a ficheros en red de forma eficiente mediante [OPenDAP](http://www.opendap.org/) o [THREDDS](http://www.unidata.ucar.edu/Projects/THREDDS/tech/TDS.html), se puede acceder o escribir ficheros netCDF-4 de [forma paralela](http://www.unidata.ucar.edu/software/netcdf/docs/parallel_io.html),...

**Cómo podemos acceder o crear/modificar ficheros netCDF desde python**

En python, como siempre, disponemos de múltiples opciones. Si solo queréis leer un fichero netcdf puntualmente podéis usar [scipy.io](http://docs.scipy.org/doc/scipy/reference/io.html) y, suponiendo que scipy es un paquete que tendrás instalado, no necesitas nada más. Si vas a trabajar más a menudo con ficheros de este tipo, mi recomendación es usar [netcdf4-python](http://code.google.com/p/netcdf4-python/) puesto que os resolverá la vida y además de leer os permitirá crear ficheros netcdf. Existe algún paquete más pero no los voy a citar porque creo que el anterior es el mejor con diferencia.

**¿Vamos a ver un poquito de python?**

Pues hoy no que tengo otros quehaceres :-), pero voy a enlazar a artículos donde ya se ha visto como acceder a estos datos y a la documentación de netcdf4-python:

  * [Documentación de netcdf4-python en inglés](http://netcdf4-python.googlecode.com/svn/trunk/docs/netCDF4-module.html)
  * En pybonacci: [[1]](http://pybonacci.org/2012/04/14/ejemplo-de-uso-de-basemap-y-netcdf4/), [[2]](http://pybonacci.org/2012/11/19/analisis-cluster-ii-clasificacion-no-supervisada-mediante-clasificacion-jerarquica-aglomerativa/). En español, por desgracia, no hay mucha cosa,...
  * Terceros: [[1]](http://www.esr.org/~chjiang/python.html), [[2]](http://snowball.millersville.edu/~adecaria/ESCI386P/esci386_lesson10_NetCDF-GRIB.pdf). En inglés.

**¿Y ahora qué?**

Contadnos si ya lo usáis y cómo, si no lo usáis pero pensáis que os puede resultar útil, si después de usarlo habéis encontrado otras alternativas (que no sea HDF) que os resulta mejor,... Además, como siempre, podéis usar los comentarios para pedir dudas y, si podemos, las resolvemos.

Saludos.