---
title: Como hacer Análisis de Sentimiento en español
date: 2015-11-24T11:47:34+00:00
author: Manuel Garrido
slug: como-hacer-analisis-de-sentimiento-en-espanol-2

**Este post es una continuación de un [articulo previo](http://pybonacci.org/2015/11/16/dibujando-100k-tweets-de-mi-ciudad/) donde explico como obtener y dibujar en un mapa un mapa de calor de miles de tweets enviados desde mi ciudad**

Puedes encontrar el código que he usado en [github](https://github.com/manugarri/tweets_map).

Tambien he subido el archivo de tweets obtenido en el articulo anterior para que puedas seguir este tutorial sin tener que descargarte los tweets.

En este post, me enfocaré en como hacer análisis de sentimiento (Sentiment Analysis) en español.

Hacer Sentiment Analysis en inglés es muy fácil. Hay múltiples paquetes que vienen con modelos preparados para calcular el sentimiento o polaridad de un nuevo texto (ejemplos incluyen [TextBlob](https://textblob.readthedocs.org) o [word2vec](https://code.google.com/p/word2vec/)).

Sin embargo, no tengo constancia de un modelo preparado en español, así que en este post vamos a hacer nuestro propio modelo predictivo :).

Para eso, lo primero que necesitamos es un dataset previamente categorizado. En mi caso utilicé el corpus de [TASS](http://www.sngularmeaning.team/TASS2015/tass2015.php#corpus).

TASS es un Taller de Análisis de Sentimiento en español organizado cada año por la [Sociedad Española del Procesado del Lenguaje Natural(SEPLN)](http://www.sepln.org/?lang=en).

Hay que pedir permiso para usar el corpus, por tanto no puedo compartirlo aquí. Para conseguirlo, solo hay que ponerse en contacto con los organizadores del TASS (hay un email de contacto en su pagina).

Los archivos del corpus están en formato XML y contienen miles de tweets en español con su sentimiento (polaridad). Algunos de estos archivos están enfocados en un tópico, por ejemplo política o TV.

La estructura de los archivos es similar a esta:

    <?xml version="1.0" encoding="UTF-8"?>  
    <tweets>  
     <tweet>
      <tweetid>142378325086715906</tweetid>
      <user>jesusmarana</user>
      <content><![CDATA[Portada 'Público', viernes. Fabra al banquillo por 'orden' del Supremo; Wikileaks 'retrata' a 160 empresas espías. http://t.co/YtpRU0fd]]></content>
      <date>2011-12-02T00:03:32</date>
      <lang>es</lang>
      <sentiments>
       <polarity><value>N</value></polarity>
      </sentiments>
      <topics>
       <topic>política</topic>
      </topics>
     </tweet>
     <tweet>
    

los campos que nos interesan para cada tweet son el campo `content` , que tiene el contenido del tweet, y el campo `sentiment.polarity.value`, que incluye la polaridad del tweet.

Hay que fijarse en que diversos archivos tienen diferentes esquemas dependiendo de que edición del TASS sean.

Después de procesar y unir todos los archivos, tenemos un archivo con unos 48,000 tweets con una polaridad asociada. Dicha polaridad esta codificada como una variable ordinal que contiene uno de los siguientes valores: `N+` (muy negativo), `N` (negativo), `NEU` (Neutral), `P` (Positivo), `P+` (muy positivo).

El objetivo de este problema de Machine Learning es predecir el sentimiento de los tweets incluidos en el [archivo que creamos en el post anterior](http://blog.manugarri.com/plotting-100k-tweets-from-my-home-town/) usando el corpus de TASS como training data (datos para entrenar al modelo predictivo).

Sin embargo, antes de hacer eso, tenemos que hacer un paso más.

Si analizamos el dataset, nos damos cuenta de que hay tweets en múltiples idiomas, y por lo tanto **no podemos predecir la polaridad de tweets que no estén escritos en español mediante el corpus de TASS**

Lo que significa que tenemos que asignar el lenguaje a cada tweet, y entonces filtrar sólo aquellos que son en español.

### Detección de Lenguaje

Para asignar el lenguaje de cada tweet, he usado 3 paquetes diferentes, [langdetect](https://pypi.python.org/pypi/langdetect/1.0.1), [langid](http://github.com/saffsd/langid.py) y [Textblob](https://textblob.readthedocs.org), y solo mantuve los tweets en los que al menos un paquete decidiera que el tweet era en español.

<pre class=" language-python"><code class=" language-python">
import langid
from langdetect import detect
import textblob

def langid_safe(tweet):
    try:
        return langid.classify(tweet)[0]
    except Exception as e:
        pass
        
def langdetect_safe(tweet):
    try:
        return detect(tweet)
    except Exception as e:
        pass

def textblob_safe(tweet):
    try:
        return textblob.TextBlob(tweet).detect_language()
    except Exception as e:
        pass   
        
#Este paso tarda mucho tiempo
tweets['lang_langid'] = tweets.tweet.apply(langid_safe)
tweets['lang_langdetect'] = tweets.tweet.apply(langdetect_safe)
tweets['lang_textblob'] = tweets.tweet.apply(textblob_safe)

tweets.to_csv('tweets_parsed2.csv', encoding='utf-8')

tweets = tweets.query("lang_langdetect == 'es' or lang_langid == 'es' or lang_langtextblob=='es' ")
</code></pre>

# Tras filtar los archivos por lenguaje nos queda un archivo de 77,550 tweets en español.

Como he mencionado más arriba, el corpus contiene múltiples niveles de polaridad. No obstante, hay diferencias entre diferentes archivos, por ejemplo algunos archivos sólo tienen los niveles _Positivo, Negativo y Neutral_

Por lo tanto para poder trabajar con todos los archivos conjuntamente, vamos a convertir la polaridad en una variable dicotómica (binaria) con los valores _(Positivo=1, Negativo=0)_.

### Procesamiento de texto

Para poder analyzar los tweets, tenemos que extraer y estructurar la información contenida en el texto. Para ello, usaremos la clase [sklearn.feature_extraction.CountVectorizer](http://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.CountVectorizer.html).

`CountVectorizer` convierte la columna de texto en una matriz en la que cada palabra es una columna cuyo valor es el número de veces que dicha palabra aparece en cada tweet.

Por ejemplo, si tenemos el tweet:

`Machine Learning is very cool`

`CountVectorizer` lo convierte en:

<table border="1" style="text-align: center;width:100%">
  <tr>
    <th>
    </th>
    
    <th>
      tweet
    </th>
    
    <th>
      machine
    </th>
    
    <th>
      learning
    </th>
    
    <th>
      is
    </th>
    
    <th>
      very
    </th>
    
    <th>
      cool
    </th>
  </tr>
  
  <tr>
    <th>
    </th>
    
    <td>
      Machine Learning is very cool
    </td>
    
    <td>
      1
    </td>
    
    <td>
      1
    </td>
    
    <td>
      1
    </td>
    
    <td>
      1
    </td>
    
    <td>
      1
    </td>
  </tr>
  
  <tr>
    <th>
      1
    </th>
    
    <td>
      Machine Learning is cool
    </td>
    
    <td>
      1
    </td>
    
    <td>
      1
    </td>
    
    <td>
      1
    </td>
    
    <td>
    </td>
    
    <td>
      1
    </td>
  </tr>
</table>



De esta forma podemos trabajar con estos vectores en vez de con texto plano.

Modificaremos nuestro `CountVectorizer` para que aplique los siguientes pasos a cada tweet:

  1. Tokenizar, este paso convierte una cadena de texto en una lista de palabras _(tokens)_. Usaremos un tokenizador modificado que no solo tokeniza (mediante el uso de `nltk.word_tokenize`), sino que también remueve signos de puntuación. Como estamos tratando con tweets en español, es importante incluir `¿` y `¡` en la lista de signos a eliminar.
  2. Convertir todas las palabras en minúsculas.
  3. Remover stopwords. Se llama stopwords a las palabras que son muy frecuentes pero que no aportan gran valor sintáctico. Ejemplos de stopwords serían _de, por, con ..._ 
  4. Stemming. Stemming es el proceso por el cual transformamos cada palabra en su raiz. Por ejemplo las palabras _maravilloso, maravilla o maravillarse_ comparten la misma raíz y se consideran la misma palabra tras el stemming.

Este es el código para procesar el texto:

<pre class=" language-python"><code class=" language-python">
#Tienes que descargarte las stopwords primero via nltk.download()
import nltk
from nltk.corpus import stopwords
from nltk import word_tokenize
from nltk.data import load
from nltk.stem import SnowballStemmer
from string import punctuation
from sklearn.feature_extraction.text import CountVectorizer       


spanish_stopwords = stopwords.words('spanish')

stemmer = SnowballStemmer('spanish')

non_words = list(punctuation)
non_words.extend(['¿', '¡'])
non_words.extend(map(str,range(10)))

stemmer = SnowballStemmer('spanish')
def stem_tokens(tokens, stemmer):
    stemmed = []
    for item in tokens:
        stemmed.append(stemmer.stem(item))
    return stemmed

def tokenize(text):
    text = ''.join([c for c in text if c not in non_words])
    tokens =  word_tokenize(text)

    # stem
    try:
        stems = stem_tokens(tokens, stemmer)
    except Exception as e:
        print(e)
        print(text)
        stems = ['']
    return stems
    
vectorizer = CountVectorizer(
                analyzer = 'word',
                tokenizer = tokenize,
                lowercase = True,
                stop_words = spanish_stopwords)
</code></pre>

### Evaluación del modelo

En este apartado es donde probamos múltiples algoritmos y medimos su eficacia. Herramientas como [SciKit-Learn Laboratory (SKLL)](https://github.com/EducationalTestingService/skll) ayudan mucho en este proceso.

Un aspecto importante a considerar es elegir una métrica apropiada para evaluar cada modelo. Como este problema es un problema de clasificación binaria _(predecir si un tweet es positivo =1 o negativo=0)_, una buena métrica es el **[Area bajo la Curva ROC](http://www.hrc.es/bioest/roc_1.html)**, que tiene en cuenta tanto los Falsos positivos (es decir, tweets negativos que fueron clasificados como positivos) como los Falsos Negativos (es decir, los tweets postivos que fueron clasificados como negativos)

Tras evaluar varios modelos, el algoritmo SVM (en particular su implementación para casos de clasificación [`LinearSVC`](http://scikit-learn.org/stable/modules/generated/sklearn.svm.LinearSVC.html) fué el que produjo valores mejores de AUC (_area under the curve_).

Una vez hemos seleccionado nuestro Vectorizer y nuestro clasificador, hacemos una búsqueda en rejilla [`GridSearchCV`](http://scikit-learn.org/stable/modules/generated/sklearn.grid_search.GridSearchCV.html). para encontrar los mejores parámetros para nuestros modelos.

`GridSearchCV` itera sobre los modelos especificados con el rango de parámetros indicado y nos devuelve aquel modelo cuyos parámetros proporcionan los mejores resultados.

Este es el código que hace la búsqueda:

<pre class=" language-python"><code class=" language-python">

#Definimos el vectorizer de nuevo y creamos un pipeline de vectorizer -&gt; classificador
vectorizer = CountVectorizer(
                analyzer = 'word',
                tokenizer = tokenize,
                lowercase = True,
                stop_words = spanish_stopwords)

#LinearSVC() es el clasificador

pipeline = Pipeline([
    ('vect', vectorizer),
    ('cls', LinearSVC()),
])


# Aqui definimos el espacio de parámetros a explorar
parameters = {
    'vect__max_df': (0.5, 1.9),
    'vect__min_df': (10, 20,50),
    'vect__max_features': (500, 1000),
    'vect__ngram_range': ((1, 1), (1, 2)),  # unigramas or bigramas
    'cls__C': (0.2, 0.5, 0.7),
    'cls__loss': ('hinge', 'squared_hinge'),
    'cls__max_iter': (500, 1000)
}


grid_search = GridSearchCV(pipeline, parameters, n_jobs=-1 , scoring='roc_auc')
grid_search.fit(tweets_corpus.content, tweets_corpus.polarity_bin)
</code></pre>

Este paso tarda bastante tiempo, pero al terminar nos devolverá el conjunto de parámetros (o como se les llama también, hiperparámetros) que producen el mejor AUC. En este caso, el mejor AUC fue de 0.92, que es un resultado aceptable (con más tiempo, intentaríamos subir ese AUC hasta los 0.97 o aproximado, pero al fin y al cabo, este es un experimento).

Ahora ya tenemos nuestros modelos con los mejores parámetros, asi que solo falta entrenar el modelo en el corpus de TASS y predecir la polaridad del archivo de tweets que descargamos.

Finalmente, guardaremos en un archivo la latitud, longitud y polaridad de cada tweet.

<pre class=" language-python"><code class=" language-python">

from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline

#Creamos un Pipeline con los parámetros mejores
pipeline = Pipeline([
    ('vect', CountVectorizer(
            analyzer = 'word',
            tokenizer = tokenize,
            lowercase = True,
            stop_words = spanish_stopwords,
            min_df = 50,
            max_df = 1.9,
            ngram_range=(1, 1),
            max_features=1000
            )),
    ('cls', LinearSVC(C=.2, loss='squared_hinge',max_iter=1000,multi_class='ovr',
             random_state=None,
             penalty='l2',
             tol=0.0001
             )),
])

#ajustamos el modelo at corpus de TASS
pipeline.fit(tweets_corpus.content, tweets_corpus.polarity_bin)
#now we predict on the new tweets dataset
tweets['polarity'] = pipeline.predict(tweets.tweet)
</code></pre>

Cuando tenemos el archivo de latitudes y longitudes con su polaridad, seguimos los mismos pasos que seguimos en el [tutorial previo](http://pybonacci.org/2015/11/16/dibujando-100k-tweets-de-mi-ciudad/) y obtenemos el siguiente mapa de calor donde se pueden observar los sitios con polaridad más negativa y más positiva:

![murcia sentiment heatmap](https://cdn.rawgit.com/manugarri/tweets_map/master/murcia_tweets_polarity.png)

¿Que os parece?