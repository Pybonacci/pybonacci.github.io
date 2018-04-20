---
title: Análisis de componentes principales con python
date: 2012-10-08T18:41:45+00:00
author: Kiko Correoso
slug: analisis-de-componentes-principales-con-python
tags: acp, analisis de componentes principales, aprendizaje automático, dimensionality reduction, Estadística, machine learning, pca, principal component analysis, python, reducción de dimensiones, scikit-learn, singular value decomposition, sklearn, svd

Esta entrada también se podría haber llamado:

'Reducción de la dimensión'

'Comprimiendo imágenes usando análisis de componentes principales y python'

**Para la siguiente entrada se ha usado python 2.7.2, numpy 1.6.1, matplotlib 1.1.0 y sklearn 0.10** 

El análisis de componentes principales (PCA, por sus siglas en inglés, Principal Component Analysis) es una técnica que trata de reducir el número de dimensiones (número de variables) de un conjunto de datos intentando, a su vez, conservar la mayor cantidad de información. Es una técnica extremadamente útil como análisis exploratorio de datos (exploratory data analysis, pongo algunos términos en inglés porque a veces pueden resultar extraños en castellano), cuando se tiene demasiada información (muchas dimensiones, variables) y no se puede analizar correctamente la información. [Se ha usado de forma exitosa para encontrar patrones, determinar 'outliers', compresión de imágenes,...](http://www.amazon.com/Principal-Component-Analysis-Statistics-ebook/dp/B003YFJ6U8) Más adelante se explicará brevemente el proceso matemático que hay detrás.

Para el presente artículo vamos a usar el PCA para obtener imágenes comprimidas. Vamos a trabajar con una imagen monocromática extraída de la galería de [AdeRussell en flickr](http://www.flickr.com/photos/aderussell/). (con [licencia cc 2.0](http://creativecommons.org/licenses/by-nc-sa/2.0/deed.es)) La imagen en cuestión es la siguiente:<figure style="width: 640px" class="wp-caption aligncenter">

[<img class="aligncenter size-full" title="King" src="http://new.pybonacci.org/images/2012/10/MartinLutherKing.jpg" alt="Martin Luther King Memorial por AdeRussell" width="640" height="425" />](http://new.pybonacci.org/images/2012/10/MartinLutherKing.jpg)

Primero la guardaremos en nuestro equipo usando la biblioteca urllib2 disponible en la biblioteca estándar de vuestra instalación de python:

<pre><code class="language-python">import urllib2
## Leemos la imagen desde la url
url = 'https://farm2.staticflickr.com/1573/26146921423_29f9a86f2b_z_d.jpg'
kk = urllib2.urlopen(url).read()
## Guardamos la imagen en el directorio donde nos encontremos
## con el nombre 'king.jpg'
imagen = open('king.jpg', 'wb')
imagen.write(kk)
imagen.close()</code></pre>

La imagen está en formato jpg, la vamos a leer usando matplotlib y vamos a guardar la información en una matriz 2D (tenemos tres canales (r,g,b) que son iguales (imagen en escala de grises) por lo que solo vamos a usar uno de ellos).

<pre><code class="language-python">import numpy as np
import matplotlib.pyplot as plt
## Leemos la imagen como un numpy array
kk = plt.imread('king.jpg')
## Si hacemos kk.shape vemos que existen
## tres canales en la imagen (r, g, b)
## Pero como es una imagen en escala de grises
## Los tres canales tienen la misma información
## por lo que nos podemos quedar con un solo canal
plt.subplot(221)
plt.title('canal 1')
plt.imshow(kk[:,:,0])
plt.subplot(222)
plt.title('canal 2')
plt.imshow(kk[:,:,1])
plt.subplot(223)
plt.title('canal 3')
plt.imshow(kk[:,:,2])
## Vemos que la imagen está rotada, hacemos uso de np.flipud
## http://docs.scipy.org/doc/numpy/reference/generated/numpy.flipud.html
plt.subplot(224)
plt.title('canal 1 rotado en BN')
plt.imshow(np.flipud(kk[:,:,0]), cmap=plt.cm.Greys_r)
plt.show()
## Finalmente, nos quedamos con una única dimensión
## Los tres canales rgb son iguales (escala de grises)
matriz = np.flipud(kk[:,:,0])</code></pre>

Bueno, ahora ya tenemos nuestra imagen como la queremos para poder empezar a trabajar con ella.

¿Cómo se obtienen las componentes principales?

<!--more-->

Pues lo mejor que podemos hacer es echarle un vistazo previo a una [explicación mejor y más completa](http://es.wikipedia.org/wiki/An%C3%A1lisis_de_componentes_principales) que la que pueda dar yo y después leer mi explicación.

¿Ya habéis leído la wikipedia? En pocas palabras, se trata de transformar nuestro conjunto de datos en un nuevo sistema de coordenadas de forma que la primera componente principal, que será la que explica la mayor varianza de los datos, corresponda al primer eje. Esto, en dos dimensiones, es sencillo de ver (cuando el número de dimensiones pasa de 3 se empieza a complicar la cosa). En la siguiente figura se muestra un scatterplot de dos variables sobre el se ha dibujado la proyección de sus dos componentes principales.

<p style="text-align:center;">
  <a href="http://es.wikipedia.org/wiki/An%C3%A1lisis_de_componentes_principales"><img class="aligncenter" src="http://upload.wikimedia.org/wikipedia/commons/thumb/1/15/GaussianScatterPCA.png/512px-GaussianScatterPCA.png" alt="" width="512" height="480" /></a>
</p>

Imaginad que en un eje tenemos datos del peso de tus vecinos y en el otro eje tenemos la altura de los mismos. En el scatterplot veríamos que existe una relación entre ambas variables. Si hacemos el análisis de las componentes principales veríamos que la primera componente explica la mayor parte de la varianza. Si nos quedásemos solo con la primera componente la podríamos interpretar como una variable 'talla' (o como la queráis llamar) que nos indica de forma aproximada lo que podría medir y pesar uno de nuestros vecinos, reduciendo las dimensiones de 2 a 1. Esto visto así es muy evidente y no haría falta usar PCA para analizar estos datos pero cuando en lugar de solo peso y altura tenemos muchas variables el análisis se complica y la interpretación de las componentes principales también. Espero que hayáis entendido algo.

Para ver una implementación del PCA usando matriz de covarianzas en python podéis echarle un ojo al siguiente artículo de [glowingpython](http://glowingpython.blogspot.com.es/2011/07/pca-and-image-compression-with-numpy.html) en el que está basado este. Nosotros no vamos a reinventar la rueda y vamos a usar la PCA que viene en el módulo [decomposition de scikits-learn.](http://scikit-learn.org/dev/modules/generated/sklearn.decomposition.PCA.html#sklearn.decomposition.PCA)  Vamos a crear un bucle para ir reconstruyendo la imagen usando diferentes números de componentes principales, de 50 en 50, para que vayáis viendo que a partir de un número de unas 100 componentes principales ya tenéis una imagen aceptable en lugar de tener que usar todas las dimensiones del conjunto de datos inicial:

<pre><code class="language-python">from sklearn.decomposition import PCA
## Leemos la imagen desde la url
for i in range(0,425,50):
pca = PCA(n_components = i)
kk = pca.fit_transform(matriz)
plt.imshow(pca.inverse_transform(kk), cmap=plt.cm.Greys_r)
plt.title(u'nº de PCs = %s' % str(i))
plt.show()</code></pre>

La siguiente imagen muestra el resultado con 100 componentes principales:

[<img class="aligncenter size-full wp-image-967" title="king-100pcs" src="http://new.pybonacci.org/images/2012/10/king-100pcs.png" alt="" width="652" height="553" srcset="https://pybonacci.org/wp-content/uploads/2012/10/king-100pcs.png 652w, https://pybonacci.org/wp-content/uploads/2012/10/king-100pcs-300x254.png 300w" sizes="(max-width: 652px) 100vw, 652px" />](http://new.pybonacci.org/images/2012/10/king-100pcs.png)

Tampoco está tan mal comparado con la imagen original de más arriba.

Por último, para que veáis la varianza explicada de cada una de las componentes principales y la varianza acumulada podéis hacer lo siguiente:

<pre><code class="language-python">pca = PCA()
pca.fit(matriz)
varianza = pca.explained_variance_ratio_
var_acum= np.cumsum(varianza)
plt.bar(range(len(varianza)), varianza)
plt.plot(range(len(varianza)), var_acum)
plt.show()</code></pre>

Para obtener el siguiente gráfico:<figure id="attachment_980" style="width: 652px" class="wp-caption aligncenter">

[<img class="size-full wp-image-980" title="varianza explicada y acumulada por las componentes principales" src="http://new.pybonacci.org/images/2012/10/varianza.png" alt="varianza explicada y acumulada por las componentes principales" width="652" height="553" srcset="https://pybonacci.org/wp-content/uploads/2012/10/varianza.png 652w, https://pybonacci.org/wp-content/uploads/2012/10/varianza-300x254.png 300w" sizes="(max-width: 652px) 100vw, 652px" />](http://new.pybonacci.org/images/2012/10/varianza.png)<figcaption class="wp-caption-text">varianza explicada y acumulada por las componentes principales</figcaption></figure> 

Con unas 30, 35 componentes principales se tendría una varianza acumulada en torno al 90% mientras que el 99% se superaría con menos de 180 componentes principales.

El código completo sería:

<pre><code class="language-python">import urllib2
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
## Leemos la imagen desde la url
url = 'https://farm2.staticflickr.com/1573/26146921423_29f9a86f2b_z_d.jpg'
kk = urllib2.urlopen(url).read()
## Guardamos la imagen en el directorio donde nos encontremos
## con el nombre 'king.jpg'
imagen = open('king.jpg', 'wb')
imagen.write(kk)
imagen.close()
## Leemos la imagen como un numpy array
kk = plt.imread('king.jpg')
## Si hacemos kk.shape vemos que existen
## tres canales en la imagen (r, g, b)
## Pero como es una imagen en escala de grises
## Los tres canales tienen la misma información
## por lo que nos podemos quedar con un solo canal
plt.subplot(221)
plt.title('canal 1')
plt.imshow(kk[:,:,0])
plt.subplot(222)
plt.title('canal 2')
plt.imshow(kk[:,:,1])
plt.subplot(223)
plt.title('canal 3')
plt.imshow(kk[:,:,2])
## Vemos que la imagen está rotada, hacemos uso de np.flipud
## http://docs.scipy.org/doc/numpy/reference/generated/numpy.flipud.html
plt.subplot(224)
plt.title('canal 1 rotado en BN')
plt.imshow(np.flipud(kk[:,:,0]), cmap=plt.cm.Greys_r)
plt.show()
## Finalmente, nos quedamos con una única dimensión
## Los tres canales rgb son iguales (escala de grises)
matriz = np.flipud(kk[:,:,0])
## Leemos la imagen desde la url
for i in range(0,425,50):
    ## Nos quedamos con i componentes principales
    pca = PCA(n_components = i)
    ## Ajustamos para reducir las dimensiones
    kk = pca.fit_transform(matriz)
    ## 'Deshacemos' y dibujamos
    plt.imshow(pca.inverse_transform(kk), cmap=plt.cm.Greys_r)
    plt.title(u'nº de PCs = %s' % str(i))
    plt.show()
pca = PCA()
pca.fit(matriz)
varianza = pca.explained_variance_ratio_
var_acum= np.cumsum(varianza)
plt.bar(range(len(varianza)), varianza)
plt.plot(range(len(varianza)), var_acum)
plt.show()</code></pre>

Espero que os sea útil y si le dais algún uso diferente al del ejemplo lo podéis comentar para que otros lo puedan ver aplicado en otros campos.

P.D.: Yo uso esto para otras cosas pero hablar o poner ejemplos siempre de mi campo profesional me parece aburrido para vosotros. Por tanto, como nunca he usado PCA para cosas como la de este ejemplo todo esto puede estar sujeto a alguna imprecisión y/o error. Si algún experto se acerca por aquí y quiere corregir algo será bienvenido el comentario.
