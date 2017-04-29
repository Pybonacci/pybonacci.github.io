---
title: Dibujando 100k tweets de mi ciudad
date: 2015-11-16T20:27:46+00:00
author: Manuel Garrido
slug: dibujando-100k-tweets-de-mi-ciudad
tags: API, heatmap, Murcia que bella eres, twitter

<div class="text_cell_render rendered_html">
  <p>
    <strong>[Esta entrada <a href="http://blog.manugarri.com/plotting-100k-tweets-from-my-home-town/">apareció originalmente en inglés en mi blog</a>].</strong>
  </p>
  
  <p>
    Hace tiempo que he querido jugar con la API de Twitter. El pasado verano se me ocurrió que podría ser interesante dibujar un mapa de mi ciudad (Murcia, España, bella ciudad con comida increible) mostrando un <em>heatmap</em> de tweets.
  </p>
  
  <p>
    La idea es que dibujando esos <em>tweets</em> podría encontrar patrones interesantes de mi ciudad. Por ejemplo:
  </p>
  
  <ul>
    <li>
      ¿Desde qué áreas la gente <em>tuitea</em> más?
    </li>
    <li>
      ¿Qué horas del día son las más activas?
    </li>
    <li>
      ¿Cuales son los lugares más felices/tristes?
    </li>
    <li>
      ¿Hay alguna comunidad <em>tuitera</em> local extranjera?
    </li>
  </ul>
  
  <p>
    Con esas ideas en la cabeza empecé la investigación. Primero, necesitaba una librería para interactuar con la API de Twitter. Después de probar la extensa cantidad de <em>wrappers</em> disponibles me decidí por <a href="http://www.tweepy.org/" target="_blank">Tweepy</a>. Posee una interfaz simple y agradable de usar y está bien mantenida.
  </p>
  
  <p>
    (INCISO, todo el código y los datos que se usan en esta entrada está disponible en <a href="https://github.com/manugarri/tweets_map" target="_blank">Github</a>).
  </p>
  
  <p>
    De cara a obtener los <em>tweets</em> de mi ciudad en tiempo real decidí ajustarme al API <em>Streaming</em> de Twitter. Este es el código sencillo que usé:
  </p>
</div>

<pre class=" language-python"><code class=" language-python">
import json
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener

ckey = CONSUMER_KEY
csecret = CONSUMER_SECRET
atoken = APP_TOKEN
asecret = APP_SECRET

murcia = [-1.157420, 37.951741, -1.081202, 38.029126] #Venid a verla, es una ciudad muy bonita!

file =  open('tweets.txt', 'a')

class listener(StreamListener):

    def on_data(self, data):
        # La API de Twitter devuelve datos en formato JSON, asi que hay que decodificarlos.
        try:
            decoded = json.loads(data)
        except Exception as e:
            print e #no queremos que el script se pare
        return True

        if decoded.get('geo') is not None:
            location = decoded.get('geo').get('coordinates')
        else:
            location = '[,]'
        text = decoded['text'].replace('\n',' ')
        user = '@' + decoded.get('user').get('screen_name')
        created = decoded.get('created_at')
        tweet = '%s|%s|%s|s\n' % (user,location,created,text)

        file.write(tweet)
        print tweet
        return True

    def on_error(self, status):
        print status

if __name__ == '__main__':
print 'Empezando...'

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
twitterStream = Stream(auth, listener())
twitterStream.filter(locations=murcia)
 </code>
</pre>

<div class="text_cell_render rendered_html">
  <p>
    El script solo requiere las claves y secretos de la API de Twitter además de un par de puntos (latitudes y longitudes de los puntos). La API de Twitter solo devolverá <em>tweets</em> cuyas lat/lon estén dentro de los límites definidos (al menos, en teoria).
  </p>
  
  <p>
    <strong>INCISO: Si no quieres tener que descargarte los tweets puedes bajarte el archivo en <a href="https://github.com/manugarri/tweets_map" target="_blank">Github</a></strong>
  </p>
  
  <p>
    Dejé este script ejecutándose durante meses en una de mis instancias en Digital Ocean. Obtuve alrededor de 600K <em>tweets</em>. De esos 600K, alrededor de 1/6 estaban geolocalizados. Por tanto, me quedé con 100K <em>tweets</em> para hacer el gráfico.
  </p>
  
  <p>
    Una vez que tenemos los datos de Twitter <em>parseados</em>, solo tuve que buscar una buena librería para dibujar <em>heatmaps</em>. La mejor que encontré, tanto por su simplicidad (solo un fichero)como por su nivel de ajustes, fue <a href="http://www.sethoscope.net/heatmap/" target="_blank">Heatmap.py</a>.
  </p>
  
  <p>
    Puedes echar un vistazo en <a href="https://github.com/manugarri/tweets_map/blob/master/3.%20Heatmap.ipynb" target="_blank">Github</a> para ver como usé <strong>heatmap</strong>. Aquí puedes varios de los mapas que dibujé:
  </p>
</div>

<img class="aligncenter" src="http://i.imgur.com/MaHKGc8.jpg" alt="" width="1014" height="1306" />
  
<img class="aligncenter" src="http://i.imgur.com/I7N3RA9.jpg" alt="" width="1015" height="1307" />

**Bonito, ¿verdad?**

En la próxima entrada os mostraré como aplicar análisis de sentimientos al conjunto de datos para encontrar los lugares de la ciudad más alegres/tristes.