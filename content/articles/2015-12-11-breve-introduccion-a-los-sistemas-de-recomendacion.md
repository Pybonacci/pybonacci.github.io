---
title: Breve introducción a los Sistemas de Recomendación
date: 2015-12-11T12:47:08+00:00
author: Manuel Garrido
slug: breve-introduccion-a-los-sistemas-de-recomendacion

En este pequeño tutorial, vamos a hablar sobre [Sistemas de Recomendación](https://es.wikipedia.org/wiki/Sistema_de_recomendaci%C3%B3n).

Es posible que no sepas que son, sin embargo interactúas constantemente con ellos en Internet.

![amazon](http://www.getvero.com/wp-content/uploads/2013/02/amazon-recommendations.jpeg)

Cada vez que Amazon te sugiere productos relacionados...

![netflix](http://core0.staticworld.net/images/article/2015/03/netflixpregodmode-100574324-orig.png)

O cuando Netflix o Youtube te recomiendan contenido que te puede interesar...

La finalidad de un sistema de recommendación es predecir la valoración que un usuario va a hacer de un ítem que todavía no ha evaluado.

Esta valoración se genera al analizar una de dos cosas, o las características de cada item, o las valoraciones de cada usuario a cada item, y se usa para recomendar contenido personalizado a los usuarios.

Hay dos tipos principales de sistemas de recomendación:

  * Filtrado de Contenido. Las recomendaciones están basadas en las características de cada item.
  * Filtrado Colaborativo. Las recomendaciones están basadas en las valoraciones existentes de los usuarios.

En este tutorial vamos a trabajar con el dataset de [MovieLens](http://grouplens.org/datasets/movielens/). Este dataset contiene valoraciones de películas sacadas de la página web MovieLens (https://movielens.org/).

El dataset consiste en múltiples archivos, pero los que vamos a usar en este artículo son _movies.dat_ y _ratings.dat_.

Primero nos descargamos el dataset:

    :::bash
    wget http://files.grouplens.org/datasets/movielens/ml-1m.zip
    unzip ml-1m.zip
    cd ml-1m/

#Filtrado de Contenido

Aquí están las primeras líneas del archivo `movies.dat`. El archivo tiene el formato:

**movie\_id::movie\_title::movie genre(s)**

<pre class=" language-bash"><code class=" language-bash">
head movies.dat

1::Toy Story (1995)::Animation|Children's|Comedy
2::Jumanji (1995)::Adventure|Children's|Fantasy
3::Grumpier Old Men (1995)::Comedy|Romance
4::Waiting to Exhale (1995)::Comedy|Drama
5::Father of the Bride Part II (1995)::Comedy
6::Heat (1995)::Action|Crime|Thriller
7::Sabrina (1995)::Comedy|Romance
8::Tom and Huck (1995)::Adventure|Children's
9::Sudden Death (1995)::Action
10::GoldenEye (1995)::Action|Adventure|Thriller
</code></pre>

Los géneros de cada película están separados por un _pipe |_.

Cargamos el archivo `movies.dat`:

<pre class=" language-python"><code class=" language-python">
import pandas as pd
import numpy as np
movies_df = pd.read_table('movies.dat', header=None, sep='::', names=['movie_id', 'movie_title', 'movie_genre'])

movies_df.head()
</code></pre>

**Out[]:**

<!--<table border="1" style="text-align: center;width:100%">-->
<table>
  <tr>
    <th>
    </th>
    
    <th>
      movie_id
    </th>
    
    <th>
      movie_title
    </th>
    
    <th>
      movie_genre
    </th>
  </tr>
  
  <tr>
    <th>
    </th>
    
    <td>
      1
    </td>
    
    <td>
      Toy Story (1995)
    </td>
    
    <td>
      Animation|Children's|Comedy
    </td>
  </tr>
  
  <tr>
    <th>
      1
    </th>
    
    <td>
      2
    </td>
    
    <td>
      Jumanji (1995)
    </td>
    
    <td>
      Adventure|Children's|Fantasy
    </td>
  </tr>
  
  <tr>
    <th>
      2
    </th>
    
    <td>
      3
    </td>
    
    <td>
      Grumpier Old Men (1995)
    </td>
    
    <td>
      Comedy|Romance
    </td>
  </tr>
  
  <tr>
    <th>
      3
    </th>
    
    <td>
      4
    </td>
    
    <td>
      Waiting to Exhale (1995)
    </td>
    
    <td>
      Comedy|Drama<br/> 
  </tr>
</table> 
      
Para poder usar la columna <code>movie_genre</code>, tenemos que convertirla en un grupo de campos llamados <code>dummy_variables</code>.
      
Esta función convierte una variable categórica (por ejemplo, el genéro de la película puede ser <em>Animation, Comedy, Romance</em>...), en múltiples columnas (una columna para <em>Animation</em>, una columna para <em>Comedy</em>, etc).

Para cada película, éstas columnas <code>dummy</code> tendrán un valor de 0 excepto para aquellos géneros que tenga la película.

    :::python
    # Convertioms los generos de peliculas a variables dummy 
    movies_df = pd.concat([movies_df, movies_df.movie_genre.str.get_dummies(sep='|')], axis=1)
    movies_df.head()
      
**Out[]:**
<table border="1" style="text-align: center;width:100%">
<tr>
  <th>
  </th>
  
  <th>
    movie_id
  </th>
  
  <th>
    movie_title
  </th>
  
  <th>
    movie_genre
  </th>
  
  <th>
    Action
  </th>
  
  <th>
    Adventure
  </th>
  
  <th>
    Animation
  </th>
  
  <th>
    Children's
  </th>
  
  <th>
    Comedy
  </th>
  
  <th>
    Crime
  </th>
  
  <th>
    Documentary
  </th>
  
  <th>
    ...
  </th>
</tr>

<tr>
  <th>
  </th>
  
  <td>
    1
  </td>
  
  <td>
    Toy Story (1995)
  </td>
  
  <td>
    Animation|Children's|Comedy
  </td>
  
  <td>
  </td>
  
  <td>
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
  </td>
  
  <td>
    ...
  </td>
</tr>

<tr>
  <th>
    1
  </th>
  
  <td>
    2
  </td>
  
  <td>
    Jumanji (1995)
  </td>
  
  <td>
    Adventure|Children's|Fantasy
  </td>
  
  <td>
  </td>
  
  <td>
    1
  </td>
  
  <td>
  </td>
  
  <td>
    1
  </td>
  
  <td>
  </td>
  
  <td>
  </td>
  
  <td>
  </td>
  
  <td>
    ...
  </td>
</tr>

<tr>
  <th>
    2
  </th>
  
  <td>
    3
  </td>
  
  <td>
    Grumpier Old Men (1995)
  </td>
  
  <td>
    Comedy|Romance
  </td>
  
  <td>
  </td>
  
  <td>
  </td>
  
  <td>
  </td>
  
  <td>
  </td>
  
  <td>
    1
  </td>
  
  <td>
  </td>
  
  <td>
  </td>
  
  <td>
    ...
  </td>
</tr>

<tr>
  <th>
    3
  </th>
  
  <td>
    4
  </td>
  
  <td>
    Waiting to Exhale (1995)
  </td>
  
  <td>
    Comedy|Drama
  </td>
  
  <td>
  </td>
  
  <td>
  </td>
  
  <td>
  </td>
  
  <td>
  </td>
  
  <td>
    1
  </td>
  
  <td>
  </td>
  
  <td>
  </td>
  
  <td>
    ...
  </td>
</tr>

<tr>
  <th>
    4
  </th>
  
  <td>
    5
  </td>
  
  <td>
    Father of the Bride Part II (1995)
  </td>
  
  <td>
    Comedy
  </td>
  
  <td>
  </td>
  
  <td>
  </td>
  
  <td>
  </td>
  
  <td>
  </td>
  
  <td>
    1
  </td>
  
  <td>
  </td>
  
  <td>
  </td>
  
  <td>
    ...
  </td>
</tr>
</table>

Por ejemplo, la película con una <code>id</code> de 1, <strong>Toy Story</strong>, pertenece a los géneros <em>Animation, Children's y Comedy</em>, y por lo tanto las columnas <em>Animation, Children's y Comedy</em> tienen un valor de 1 para Toy Story.
      
<pre class=" language-python"> <code class=" language-python">
movie_categories = movies_df.columns[3:]
movies_df.loc[0]
</code></pre>
 
**Out[]:**

<pre><code>
movie_id                                 1
movie_title               Toy Story (1995)
movie_genre    Animation|Children&apos;s|Comedy
Action                                   0
Adventure                                0
Animation                                1
Children&apos;s                          1
Comedy                                   1
Crime                                    0
Documentary                              0
Drama                                    0
Fantasy                                  0
Film-Noir                                0
Horror                                   0
Musical                                  0
Mystery                                  0
Romance                                  0
Sci-Fi                                   0
Thriller                                 0
War                                      0
Western                                  0
Name: 0, dtype: object
</code></pre>
      
El filtrado de contenidos es una manera bastante simple de construir un sistema de recomendación. En este método, los items (en éste ejemplo las películas), se asocian a un grupo de características (en este caso los géneros cinematográficos).

Para recomendar items a un usuario, primero dicho usuario tiene que especificar sus preferencias en cuanto a las características.
      
En el ejemplo de Movielens, el usuario tiene que especificar qué generos le gustan y cuánto le gustan.

Por el momento tenemos todas las columnas categorizadas por géneros.

Vamos a crear un usuario de ejemplo, con unos gustos cinematográficos enfocados a películas de acción, aventura y ficción:
      
<pre class=" language-python"> <code class=" language-python">
from collections import OrderedDict

user_preferences = OrderedDict(zip(movie_categories, []))

user_preferences['Action'] = 5
user_preferences['Adventure'] = 5
user_preferences['Animation'] = 1
user_preferences["Children's"] = 1
user_preferences["Comedy"] = 3
user_preferences['Crime'] = 2
user_preferences['Documentary'] = 1
user_preferences['Drama'] = 1
user_preferences['Fantasy'] = 5
user_preferences['Film-Noir'] = 1
user_preferences['Horror'] = 2
user_preferences['Musical'] = 1
user_preferences['Mystery'] = 3
user_preferences['Romance'] = 1
user_preferences['Sci-Fi'] = 5
user_preferences['War'] = 3
user_preferences['Thriller'] = 2
user_preferences['Western'] =1
</code></pre>
      
Ahora que tenemos las preferencias del usuario, para calcular la puntuación que dicho usuario daría a cada película sólo tenemos que hacer el producto vectorial de las preferencias del usuario con las características de cada película.
      
<pre class=" language-python"> <code class=" language-python">
#En producción usaríamos np.dot, en vez de escribir esta función, la pongo como ejemplo.
def dot_product(vector_1, vector_2):
    return sum([ i*j for i,j in zip(vector_1, vector_2)])

def get_movie_score(movie_features, user_preferences):
    return dot_product(movie_features, user_preferences)
</code></pre>
      
Ahora podemos computar la puntuación de la película <em>Toy Story</em>, una película de animación infantil, para el usuario del ejemplo.
      
<pre class=" language-python"> <code class=" language-python">
toy_story_features = movies_df.loc[0][movie_categories]
toy_story_features
</code></pre>
      
<pre><code>
Action         0
Adventure      0
Animation      1
Children's     1
Comedy         1
Crime          0
Documentary    0
Drama          0
Fantasy        0
Film-Noir      0
Horror         0
Musical        0
Mystery        0
Romance        0
Sci-Fi         0
Thriller       0
War            0
Western        0
Name: 0, dtype: object
</code></pre>
      
<pre class=" language-python"> <code class=" language-python">
toy_story_user_predicted_score = dot_product(toy_story_features, user_preferences.values())
toy_story_user_predicted_score
</code></pre>
      
**Out[]:**
<pre>5</pre>
      
Para este usuario, Toy Story tiene una puntuación de 5. Lo cual no significa mucho por sí mismo, sólo si comparamos dicha puntuación con la puntuación de las otras películas.
      
Por ejemplo, calculamos la puntuación de <strong>Die Hard (La Jungla de Cristal)</strong>, una película de acción.
      
<pre class=" language-python"> <code class=" language-python">
movies_df[movies_df.movie_title.str.contains('Die Hard')]
</code></pre>

<table border="1" style="text-align: center;width:100%">
<tr>
  <th>
  </th>
  
  <th>
    movie_id
  </th>
  
  <th>
    movie_title
  </th>
  
  <th>
    movie_genre
  </th>
  
  <th>
    Action
  </th>
  
  <th>
    Adventure
  </th>
  
  <th>
    Animation
  </th>
  
  <th>
    Children's
  </th>
  
  <th>
    Comedy
  </th>
  
  <th>
    Crime
  </th>
  
  <th>
    Documentary
  </th>
  
  <th>
    ...
  </th>
</tr>

<tr>
  <th>
    163
  </th>
  
  <td>
    165
  </td>
  
  <td>
    Die Hard: With a Vengeance (1995)
  </td>
  
  <td>
    Action|Thriller
  </td>
  
  <td>
    1
  </td>
  
  <td>
  </td>
  
  <td>
  </td>
  
  <td>
  </td>
  
  <td>
  </td>
  
  <td>
  </td>
  
  <td>
  </td>
  
  <td>
    ...
  </td>
</tr>

<tr>
  <th>
    1023
  </th>
  
  <td>
    1036
  </td>
  
  <td>
    Die Hard (1988)
  </td>
  
  <td>
    Action|Thriller
  </td>
  
  <td>
    1
  </td>
  
  <td>
  </td>
  
  <td>
  </td>
  
  <td>
  </td>
  
  <td>
  </td>
  
  <td>
  </td>
  
  <td>
  </td>
  
  <td>
    ...
  </td>
</tr>

<tr>
  <th>
    1349
  </th>
  
  <td>
    1370
  </td>
  
  <td>
    Die Hard 2 (1990)
  </td>
  
  <td>
    Action|Thriller
  </td>
  
  <td>
    1
  </td>
  
  <td>
  </td>
  
  <td>
  </td>
  
  <td>
  </td>
  
  <td>
  </td>
  
  <td>
  </td>
  
  <td>
  </td>
  
  <td>
    ...
  </td>
</tr>
</table>

<pre class=" language-python"> <code class=" language-python">
die_hard_id = 1036
die_hard_features = movies_df[movies_df.movie_id==die_hard_id][movie_categories]
die_hard_features.T 
</code></pre>
      
**Out[]:**
      
<table border="1" style="text-align: center">
<tr>
  <th>
  </th>
  
  <th>
    1023
  </th>
</tr>

<tr>
  <th>
    Action
  </th>
  
  <td>
    1
  </td>
</tr>

<tr>
  <th>
    Adventure
  </th>
  
  <td>
  </td>
</tr>

<tr>
  <th>
    Animation
  </th>
  
  <td>
  </td>
</tr>

<tr>
  <th>
    Children's
  </th>
  
  <td>
  </td>
</tr>

<tr>
  <th>
    Comedy
  </th>
  
  <td>
  </td>
</tr>

<tr>
  <th>
    Crime
  </th>
  
  <td>
  </td>
</tr>

<tr>
  <th>
    Documentary
  </th>
  
  <td>
  </td>
</tr>

<tr>
  <th>
    Drama
  </th>
  
  <td>
  </td>
</tr>

<tr>
  <th>
    Fantasy
  </th>
  
  <td>
  </td>
</tr>

<tr>
  <th>
    Film-Noir
  </th>
  
  <td>
  </td>
</tr>

<tr>
  <th>
    Horror
  </th>
  
  <td>
  </td>
</tr>

<tr>
  <th>
    Musical
  </th>
  
  <td>
  </td>
</tr>

<tr>
  <th>
    Mystery
  </th>
  
  <td>
  </td>
</tr>

<tr>
  <th>
    Romance
  </th>
  
  <td>
  </td>
</tr>

<tr>
  <th>
    Sci-Fi
  </th>
  
  <td>
  </td>
</tr>

<tr>
  <th>
    Thriller
  </th>
  
  <td>
    1
  </td>
</tr>

<tr>
  <th>
    War
  </th>
  
  <td>
  </td>
</tr>

<tr>
  <th>
    Western
  </th>
  
  <td>
  </td>
</tr>
</table>

*Nota, 1023 es el índice interno del dataframe, no el índice de la película Die Hard en Movielens*
      
<pre class=" language-python"> <code class=" language-python">
die_hard_user_predicted_score = dot_product(die_hard_features.values[0], user_preferences.values())
die_hard_user_predicted_score
</code></pre>
      
**Out[]:**
<pre>8</pre>
      
Vemos que Die Hard tiene una puntuación de 8 y Toy Story de 5, asi que Die Hard sería recomendada al usuario antes que Toy Story. Lo cual tiene sentido teniendo en cuenta que a nuestro usuario de ejemplo le encantan las películas de acción.
      
Una vez sabemos como calcular la puntuación para una película, recomendar nuevas películas es tan fácil como calcular las puntuaciones de cada película, y luego escoger aquellas con una puntuación más alta.
      
<pre class=" language-python"> <code class=" language-python">
def get_movie_recommendations(user_preferences, n_recommendations):
    #we add a column to the movies_df dataset with the calculated score for each movie for the given user
    movies_df['score'] = movies_df[movie_categories].apply(get_movie_score, 
                                                           args=([user_preferences.values()]), axis=1)
    return movies_df.sort_values(by=['score'], ascending=False)['movie_title'][:n_recommendations]
    
get_movie_recommendations(user_preferences, 10)    
</code></pre>
      
**Out[]:**
      
<pre><code>
2253                                       Soldier (1998)
257             Star Wars: Episode IV - A New Hope (1977)
2036                                          Tron (1982)
1197                              Army of Darkness (1993)
2559     Star Wars: Episode I - The Phantom Menace (1999)
1985                      Honey, I Shrunk the Kids (1989)
1192    Star Wars: Episode VI - Return of the Jedi (1983)
1111                                    Abyss, The (1989)
1848                                    Armageddon (1998)
2847                                  Total Recall (1990)
Name: movie_title, dtype: object&lt;/pre&gt;
</code></pre>
      
Asi que vemos que el sistema de recomendación recomienda películas de acción y de ciencia ficción.

El filtrado de contenidos hace que recomendar nuevas películas a un usuario sea muy fácil, ya que los usuarios simplemente tienen que indicar sus preferencias una vez. Sin embargo, este sistema tiene algunos problemas:
      
- Hay que categorizar cada item nuevo manualmente en funcion a las características existentes.
- Las recomendaciones son limitadas, ya que por ejemplo, los items existentes no se pueden clasificar en función de una nueva categoría.
        
Hemos visto que el filtrado de contenidos es quizás una manera demasiado simple de hacer recomendaciones, lo que nos lleva a...
      
#Filtrado Colaborativo
      
El filtrado colaborativo es otro método distinto de predecir puntuaciones de usuarios a items. Sin embrago, en este método usamos las puntuaciones existentes de usuarios a items para predecir los items que no han sido valorados por el usuario al que queremos recomendar.
      
Para ello asumimos que las recomendaciones que le hagamos a un usuario serán mejores si las basamos en usuarios con gustos similares.
      
Para este ejemplo usaremos el archivo <em>ratings.dat</em>, que tiene el siguiente formato:
      
**user_id::movie_id::rating::timestamp**
      
<pre><code>head ratings.dat

1::1193::5::978300760
1::661::3::978302109
1::914::3::978301968
1::3408::4::978300275
1::2355::5::978824291
1::1197::3::978302268
1::1287::5::978302039
1::2804::5::978300719
1::594::4::978302268
1::919::4::978301368
</code></pre>
      
El dataset de Movielens contiene un archivo con más de un millón de valoraciones de películas hechas por usuarios.
      
<pre class=" language-python"> <code class=" language-python">
ratings_df = pd.read_table('ratings.dat', header=None, sep='::', names=['user_id', 'movie_id', 'rating', 'timestamp'])

#Borramos al fecha en la que el rating fue creado.
del ratings_df['timestamp']

#reemplazamos la id de la película por su titulo para tener una mayor claridad
ratings_df = pd.merge(ratings_df, movies_df, on='movie_id')[['user_id', 'movie_title', 'movie_id','rating']]

ratings_df.head()
</code></pre>
      
**Out[]:**
      
<table border="1" style="text-align: center;width:100%">
<tr>
  <th>
  </th>
  
  <th>
    user_id
  </th>
  
  <th>
    movie_title
  </th>
  
  <th>
    movie_id
  </th>
  
  <th>
    rating
  </th>
</tr>

<tr>
  <th>
  </th>
  
  <td>
    1
  </td>
  
  <td>
    One Flew Over the Cuckoo's Nest (1975)
  </td>
  
  <td>
    1193
  </td>
  
  <td>
    5
  </td>
</tr>

<tr>
  <th>
    1
  </th>
  
  <td>
    2
  </td>
  
  <td>
    One Flew Over the Cuckoo's Nest (1975)
  </td>
  
  <td>
    1193
  </td>
  
  <td>
    5
  </td>
</tr>

<tr>
  <th>
    2
  </th>
  
  <td>
    12
  </td>
  
  <td>
    One Flew Over the Cuckoo's Nest (1975)
  </td>
  
  <td>
    1193
  </td>
  
  <td>
    4
  </td>
</tr>

<tr>
  <th>
    3
  </th>
  
  <td>
    15
  </td>
  
  <td>
    One Flew Over the Cuckoo's Nest (1975)
  </td>
  
  <td>
    1193
  </td>
  
  <td>
    4
  </td>
</tr>

<tr>
  <th>
    4
  </th>
  
  <td>
    17
  </td>
  
  <td>
    One Flew Over the Cuckoo's Nest (1975)
  </td>
  
  <td>
    1193
  </td>
  
  <td>
    5
  </td>
</tr>
</table>

De momento tenemos una matriz de usuarios y películas, vamos a convertir <code>ratings_df</code> a una matriz con un usuario por fila y una película por columna.
      
<pre class=" language-python"> <code class=" language-python">
ratings_mtx_df = ratings_df.pivot_table(values='rating', index='user_id', columns='movie_title')
ratings_mtx_df.fillna(0, inplace=True)

movie_index = ratings_mtx_df.columns

ratings_mtx_df.head()
</code></pre>
      
**Out[]:**

<table border="1" class="dataframe">
<tr style="text-align: right">
  <th>
    movie_title
  </th>
  
  <th>
    $1,000,000 Duck (1971)
  </th>
  
  <th>
    'Night Mother (1986)
  </th>
  
  <th>
    'Til There Was You (1997)
  </th>
  
  <th>
    ...
  </th>
</tr>

<tr>
  <th>
    user_id
  </th>
  
  <th>
  </th>
  
  <th>
  </th>
  
  <th>
  </th>
  
  <th>
  </th>
</tr>

<tr>
  <th>
    1
  </th>
  
  <td>
  </td>
  
  <td>
  </td>
  
  <td>
  </td>
  
  <td>
    ...
  </td>
</tr>

<tr>
  <th>
    2
  </th>
  
  <td>
  </td>
  
  <td>
  </td>
  
  <td>
  </td>
  
  <td>
    ...
  </td>
</tr>

<tr>
  <th>
    3
  </th>
  
  <td>
  </td>
  
  <td>
    5
  </td>
  
  <td>
  </td>
  
  <td>
    ...
  </td>
</tr>

<tr>
  <th>
    4
  </th>
  
  <td>
  </td>
  
  <td>
  </td>
  
  <td>
    1
  </td>
  
  <td>
    ...
  </td>
</tr>

<tr>
  <th>
    5
  </th>
  
  <td>
  </td>
  
  <td>
  </td>
  
  <td>
  </td>
  
  <td>
    ...
  </td>
</tr>
</table>

Nos queda una matriz de 6064 usuarios y 3706 películas.

Para computar la similaridad entre películas, una manera de hacerlo es calcular la correlación entre ellas en función de la puntuación que dan los usuarios.

Una manera fácil de calcular la similaridad en python es usando la función <code>numpy.corrcoef</code>, que calcula el coeficiente de correlación de Pearson(PMCC)](https://es.wikipedia.org/wiki/Coeficiente_de_correlaci%C3%B3n_de_Pearson) entre cada pareja de items.
      
El PMCC tiene un valor entre -1 y 1 que mide cuán relacionadas están un par de variables cuantitativas.
      
La matriz de correlación es una matriz de tamaño <em>m x m</em>, donde el elemento <em>Mij</em> representa la correlación entre el item i y el item j.
      
<pre class=" language-python"> <code class=" language-python">
corr_matrix = np.corrcoef(ratings_mtx_df.T)
corr_matrix.shape
</code></pre>
      
**Out[]:**
      
<pre><code>(3706, 3706)</code></pre>
      
*Nota: Usamos la matriz traspuesta de <code>ratings_mtx_df</code> para que la función <code>np.corrcoef</code> nos devuelva la correlación entre películas. En caso de no hacerlo nos devolvería la correlación entre usuarios.*
      
Una vez tenemos la matriz, si queremos encontrar películas similares a una concreta, solo tenemos que encontrar las películas con una correlación alta con ésta.
      
<pre class=" language-python"> <code class=" language-python">
favoured_movie_title = 'Toy Story (1995)'

favoured_movie_index = list(movie_index).index(favoured_movie_title)

P = corr_matrix[favoured_movie_index]

#solo devolvemos las películas con la mayor correlación con Toy Story
list(movie_index[(P&gt;0.4) & (P&lt;1.0)])
</code></pre>
      
**Out[]:**
      
<pre><code>
['Aladdin (1992)',
 "Bug's Life, A (1998)",
 'Groundhog Day (1993)',
 'Lion King, The (1994)',
 'Toy Story 2 (1999)']
</code></pre>
      
Vemos que los resultados son bastante buenos.
      
Ahora, si queremos recomendar películas a un usuario, solo tenemos que conseguir la lista de películas que dicho usuario ha visto. Ahora, con dicha lista, podemos sumar las correlaciones de dichas películas con todas las demás y devolver las películas con una mayor correlación total.
      
<pre class=" language-python"> <code class=" language-python">
def get_movie_similarity(movie_title):
    '''Devuelve el vector de correlación para una película'''
    movie_idx = list(movie_index).index(movie_title)
    return corr_matrix[movie_idx]

def get_movie_recommendations(user_movies):
    '''Dado un grupo de películas, devolver las mas similares'''
    movie_similarities = np.zeros(corr_matrix.shape[0])
    for movie_id in user_movies:
        movie_similarities = movie_similarities + get_movie_similarity(movie_id)
    similarities_df = pd.DataFrame({
        'movie_title': movie_index,
        'sum_similarity': movie_similarities
        })
    similarities_df = similarities_df[~(similarities_df.movie_title.isin(user_movies))]
    similarities_df = similarities_df.sort_values(by=['sum_similarity'], ascending=False)
    return similarities_df
</code></pre>
      
Por ejemplo, vamos a seleccionar un usuario con preferencia por las películas infantiles y algunas películas de acción.
      
<pre class=" language-python"> <code class=" language-python">
sample_user = 21
ratings_df[ratings_df.user_id==sample_user].sort_values(by=['rating'], ascending=False)
</code></pre>
      
**Out[]:**

<table border="1" style="text-align: center;width:100%">
<tr>
  <th>
  </th>
  
  <th>
    user_id
  </th>
  
  <th>
    movie_title
  </th>
  
  <th>
    movie_id
  </th>
  
  <th>
    rating
  </th>
</tr>

<tr>
  <th>
    583304
  </th>
  
  <td>
    21
  </td>
  
  <td>
    Titan A.E. (2000)
  </td>
  
  <td>
    3745
  </td>
  
  <td>
    5
  </td>
</tr>

<tr>
  <th>
    707307
  </th>
  
  <td>
    21
  </td>
  
  <td>
    Princess Mononoke, The (Mononoke Hime) (1997)
  </td>
  
  <td>
    3000
  </td>
  
  <td>
    5
  </td>
</tr>

<tr>
  <th>
    70742
  </th>
  
  <td>
    21
  </td>
  
  <td>
    Star Wars: Episode VI - Return of the Jedi (1983)
  </td>
  
  <td>
    1210
  </td>
  
  <td>
    5
  </td>
</tr>

<tr>
  <th>
    239644
  </th>
  
  <td>
    21
  </td>
  
  <td>
    South Park: Bigger, Longer and Uncut (1999)
  </td>
  
  <td>
    2700
  </td>
  
  <td>
    5
  </td>
</tr>

<tr>
  <th>
    487530
  </th>
  
  <td>
    21
  </td>
  
  <td>
    Mad Max Beyond Thunderdome (1985)
  </td>
  
  <td>
    3704
  </td>
  
  <td>
    4
  </td>
</tr>

<tr>
  <th>
    707652
  </th>
  
  <td>
    21
  </td>
  
  <td>
    Little Nemo: Adventures in Slumberland (1992)
  </td>
  
  <td>
    2800
  </td>
  
  <td>
    4
  </td>
</tr>

<tr>
  <th>
    708015
  </th>
  
  <td>
    21
  </td>
  
  <td>
    Stop! Or My Mom Will Shoot (1992)
  </td>
  
  <td>
    3268
  </td>
  
  <td>
    3
  </td>
</tr>

<tr>
  <th>
    706889
  </th>
  
  <td>
    21
  </td>
  
  <td>
    Brady Bunch Movie, The (1995)
  </td>
  
  <td>
    585
  </td>
  
  <td>
    3
  </td>
</tr>

<tr>
  <th>
    623947
  </th>
  
  <td>
    21
  </td>
  
  <td>
    Iron Giant, The (1999)
  </td>
  
  <td>
    2761
  </td>
  
  <td>
    3
  </td>
</tr>

<tr>
  <th>
    619784
  </th>
  
  <td>
    21
  </td>
  
  <td>
    Wild Wild West (1999)
  </td>
  
  <td>
    2701
  </td>
  
  <td>
    3
  </td>
</tr>

<tr>
  <th>
    4211
  </th>
  
  <td>
    21
  </td>
  
  <td>
    Bug's Life, A (1998)
  </td>
  
  <td>
    2355
  </td>
  
  <td>
    3
  </td>
</tr>

<tr>
  <th>
    368056
  </th>
  
  <td>
    21
  </td>
  
  <td>
    Akira (1988)
  </td>
  
  <td>
    1274
  </td>
  
  <td>
    3
  </td>
</tr>

<tr>
  <th>
    226126
  </th>
  
  <td>
    21
  </td>
  
  <td>
    Who Framed Roger Rabbit? (1988)
  </td>
  
  <td>
    2987
  </td>
  
  <td>
    3
  </td>
</tr>

<tr>
  <th>
    41633
  </th>
  
  <td>
    21
  </td>
  
  <td>
    Toy Story (1995)
  </td>
  
  <td>
    1
  </td>
  
  <td>
    3
  </td>
</tr>

<tr>
  <th>
    34978
  </th>
  
  <td>
    21
  </td>
  
  <td>
    Aladdin (1992)
  </td>
  
  <td>
    588
  </td>
  
  <td>
    3
  </td>
</tr>

<tr>
  <th>
    33432
  </th>
  
  <td>
    21
  </td>
  
  <td>
    Antz (1998)
  </td>
  
  <td>
    2294
  </td>
  
  <td>
    3
  </td>
</tr>

<tr>
  <th>
    18917
  </th>
  
  <td>
    21
  </td>
  
  <td>
    Bambi (1942)
  </td>
  
  <td>
    2018
  </td>
  
  <td>
    1
  </td>
</tr>

<tr>
  <th>
    612215
  </th>
  
  <td>
    21
  </td>
  
  <td>
    Devil's Advocate, The (1997)
  </td>
  
  <td>
    1645
  </td>
  
  <td>
    1
  </td>
</tr>

<tr>
  <th>
    617656
  </th>
  
  <td>
    21
  </td>
  
  <td>
    Prince of Egypt, The (1998)
  </td>
  
  <td>
    2394
  </td>
  
  <td>
    1
  </td>
</tr>

<tr>
  <th>
    440983
  </th>
  
  <td>
    21
  </td>
  
  <td>
    Pinocchio (1940)
  </td>
  
  <td>
    596
  </td>
  
  <td>
    1
  </td>
</tr>

<tr>
  <th>
    707674
  </th>
  
  <td>
    21
  </td>
  
  <td>
    Messenger: The Story of Joan of Arc, The (1999)
  </td>
  
  <td>
    3053
  </td>
  
  <td>
    1
  </td>
</tr>

<tr>
  <th>
    708194
  </th>
  
  <td>
    21
  </td>
  
  <td>
    House Party 2 (1991)
  </td>
  
  <td>
    3774
  </td>
  
  <td>
    1
  </td>
</tr>
</table>

Ahora podemos proporcionar nuevas recomendaciones para dicho usuario teniendo en cuenta las películas que ha visto como input.
      
<pre class=" language-python"> <code class=" language-python">
sample_user_movies = ratings_df[ratings_df.user_id==sample_user].movie_title.tolist()
recommendations = get_movie_recommendations(sample_user_movies)

#Obtenemos las 20 películas con mejor puntuación
recommendations.movie_title.head(20)
</code></pre>
      
**Out[]:**
      
<pre><code>
1939                     Lion King, The (1994)
324                Beauty and the Beast (1991)
1948                Little Mermaid, The (1989)
3055    Snow White and the Seven Dwarfs (1937)
647                     Charlotte&apos;s Web (1973)
679                          Cinderella (1950)
1002                              Dumbo (1941)
301                              Batman (1989)
3250            Sword in the Stone, The (1963)
303                      Batman Returns (1992)
2252                              Mulan (1998)
2924                Secret of NIMH, The (1982)
2808                         Robin Hood (1973)
3026                    Sleeping Beauty (1959)
1781                   Jungle Book, The (1967)
260         Back to the Future Part III (1990)
259          Back to the Future Part II (1989)
2558                          Peter Pan (1953)
2347             NeverEnding Story, The (1984)
97                  Alice in Wonderland (1951)
Name: movie_title, dtype: object
</code></pre>
      
Vemos que el sistema recomienda mayoritariamente películas infantiles y algunas películas de acción.
      
El ejemplo que he puesto sobre filtrado colaborativo es un ejemplo muy simple, y no tiene en cuenta las valoraciones que cada usuario ha hecho a cada película (solo si las ha visto).
      
Una manera más eficaz de hacer filtrado colaborativo es vía <a href="https://es.wikipedia.org/wiki/Descomposici%C3%B3n_en_valores_singulares">Descomposición en valores singulares (SVD)</a>. Es un tópico que da para otro artículo pero <a href="http://www.mate.unlp.edu.ar/practicas/70_18_0911201012951">este artículo</a> lo explica con bastante claridad.

El filtrado colaborativo se usa con frecuencia en la actualidad. Es capaz de recomendar nuevos items sin tener que clasificarlos manualmente en función de sus características. Además, es capaz de proporcionar recomendaciones basadas en características ocultas que no serían obvias a primera vista (por ejemplo, combinaciones de géneros o de actores).<br /> Sin embargo, el filtrado colaborativo tiene un problema importante, y es que no puede recomendar items a un usuario a menos que dicho usuario haya valorado items, este problema se llama <a href="https://es.wikipedia.org/wiki/Arranque_en_fr%C3%ADo">problema de Arranque en frío</a>.
      
Una manera de solucionar ésto es usar un sistema híbrido de filtrado de contenido + filtrado colaborativo, usando el filtrado de contenidos para nuevos usuarios y filtrado colaborativo para usuarios de los que se tiene suficiente información.
      
#Lista de lecturas
      
Aquí hay una lista de lecturas sobre sisetmas de recomendación (en inglés)

<ul>
  <li>
    <a href="http://guidetodatamining.com/chapter2/">A Programmer's guide to Data Mining Ch:2</a>
  </li>
  <li>
    <a href="http://www.mmds.org/">Mining of Massive Datasets Ch:9. Recommendation Systems</a>
  </li>
  <li>
    <a href="http://www.cs.cmu.edu/~wcohen/collab-filtering-tutorial.ppt">Collaborative Filtering: A tutorial</a>
  </li>
</ul>
