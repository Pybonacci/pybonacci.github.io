---
title: Regex mediante ejemplos
date: 2013-02-21T19:55:56+00:00
author: Kiko Correoso
slug: regex-mediante-ejemplos
tags: expresiones regulares, python, re, regex, regexp

Las expresiones regulares, regex o regexp siempre me han parecido algo especialmente críptico. La realidad es que nunca les dediqué un mínimo de tiempo ya que en el trabajo todo es para ayer y siempre acabo acudiendo a soluciones 'stackoverfloweras' donde los super expertos siempre están ahí ([gracias chicos](http://python.majibu.org/preguntas/2122/reemplazar-patron-usando-expresiones-regulares)). Pero se acabó, aprovechando que estoy en un avión y tengo unas horas y que me he planificado y descargado varios recursos previamente para poder trabajar 'offline' voy a aprovechar para intentar que lo aprendamos o, al menos, nos introduzcamos en ello mediante ejemplos y, así, nos acerquemos más a ser unos expertos mineros de datos y podamos extraer la correcta información a analizar.

Aunque en python se puedan buscar patrones de otras formas diferentes vamos a usar el módulo [_re_](http://docs.python.org/3.3/library/re.html) de la librería estándar.

<pre><code class="language-python">import re</code></pre>

Vamos al lío. Imaginad que tenéis una cadena de e-mails en texto plano formateados de la forma que figura a continuación.

<pre><code class="language-python">texto = """
De: monete_que_no_ve@lostresmonetes.net
Enviado el: Jueves, 18 de noviembre de 2012 a las 13:22
Para: torpedo@submarino.com
Asunto: Re: Conquistar el mundo
Hola.
Aapfojewagf ajwa wjepofoisa jvgoisajigf jewapoijewagomsod moisjaoigjpoewijsn dsanigeaoi.
Ajfpoijwafe sodvm osznfinewahaw eoansjgndsakjnglkjds.
Alkjndszkng aigpiewannalkjndkjnlkjdznvns ln sa nfpoiewa npoinpewnpofn.
N&lt;sznvcknvknkxzvnoisajpoijewaoi jmsam lkvznapiunea engnal nfsl.
De: torpedo@submarino.com
Enviado el: Jueves, 18 de noviembre de 2012 a las 12:42
Para: monete_que_no_ve@lostresmonetes.net
Asunto: Re: Conquistar el mundo
Hola.
Aapfojewagf ajwa wjepofoisa jvgoisajigf jewapoijewagomsod moisjaoigjpoewijsn dsanigeaoi.
Ajfpoijwafe sodvm osznfinewahaw eoansjgndsakjnglkjds.
Alkjndszkng aigpiewannalkjndkjnlkjdznvns ln sa nfpoiewa npoinpewnpofn.
N&lt;sznvcknvknkxzvnoisajpoijewaoi jmsam lkvznapiunea engnal nfsl.
De: monete_que_no_ve@lostresmonetes.net
Enviado el: Jueves, 18 de noviembre de 2012 a las 11:57
Para: torpedo@submarino.com
Asunto: Re: Conquistar el mundo
Hola.
Aapfojewagf ajwa wjepofoisa jvgoisajigf jewapoijewagomsod moisjaoigjpoewijsn dsanigeaoi.
Ajfpoijwafe sodvm osznfinewahaw eoansjgndsakjnglkjds.
Alkjndszkng aigpiewannalkjndkjnlkjdznvns ln sa nfpoiewa npoinpewnpofn.
N&lt;sznvcknvknkxzvnoisajpoijewaoi jmsam lkvznapiunea engnal nfsl.
De: torpedo@submarino.com
Enviado el: Jueves, 18 de noviembre de 2012 a las 11:54
Para: monete_que_no_ve@lostresmonetes.net
Asunto: Re: Conquistar el mundo
Hola.
Aapfojewagf ajwa wjepofoisa jvgoisajigf jewapoijewagomsod moisjaoigjpoewijsn dsanigeaoi.
Ajfpoijwafe sodvm osznfinewahaw eoansjgndsakjnglkjds.
Alkjndszkng aigpiewannalkjndkjnlkjdznvns ln sa nfpoiewa npoinpewnpofn.
N&lt;sznvcknvknkxzvnoisajpoijewaoi jmsam lkvznapiunea engnal nfsl.
De: monete_que_no_ve@lostresmonetes.net
Enviado el: Jueves, 18 de noviembre de 2012 a las 09:15
Para: torpedo@submarino.com
Asunto: Conquistar el mundo
Hola.
Aapfojew mi primo el monete que no habla (Monete.que.no.habla@lostresmonetes.net) agf ajwa wjepofoisa jvgoisajigf.
Para la ninia + w@pa del tuenti, hoygan (Monete_que_no_escucha@lostresmonetes.co.uk).
Ajfpoijwafe sodvm osznfinewahaw eoansjgndsakjnglkjds.
Alkjndszkng aigpiewannalkjndkjnlkjdznvns ln sa nfpoiewa npoinpewnpofn.
N&lt;sznvcknvknkxzvnoisajpoijewaoi jmsam lkvznapiunea engnal nfsl.
"""</code></pre>

Imaginad que nuestro problema es que queremos saber cuantas direcciones de correo diferentes aparecen en toda la cadena de correos anterior (almacenada en la variable 'texto'. Para la cadena anterior sería sencillo hacerlo a mano, pero imaginad que hay miles de correos.

Una forma sería usar el siguiente patrón: `'S+@S+'`

donde

`'S'` encuentra cualquier caracter que no sea un espacio en blanco (en las direcciones de correo no está permitido usar espacios en blanco). Sería equivalente a usar r'[^ tnrfv]' (mirad [aquí](http://docs.python.org/3.3/library/re.html#regular-expression-syntax) para ver qué es esto último entre corchetes)

`'+'` indica que hay que encontrar al menos un caracter que no sea un espacio en blanco

`'@'` indica la arroba 🙂

No voy a hablar de ninguna de las funciones del módulo [_re_](http://docs.python.org/3.3/library/re.html) ya que para eso tenéis la documentación oficial de python. Empezaré usando la función [_findall_](http://docs.python.org/3.3/library/re.html#re.findall) para los primeros ejemplos.

<pre><code class="language-python">print(re.findall('S+@S+', texto))</code></pre>

La salida del anterior código mostrará:

<pre><code class="language-python">['monete_que_no_ve@lostresmonetes.net', 'torpedo@submarino.com', 'torpedo@submarino.com', 'monete_que_no_ve@lostresmonetes.net', 'monete_que_no_ve@lostresmonetes.net', 'torpedo@submarino.com', 'torpedo@submarino.com', 'monete_que_no_ve@lostresmonetes.net', 'monete_que_no_ve@lostresmonetes.net', 'torpedo@submarino.com', '(Monete.que.no.habla@lostresmonetes.net)', 'w@pa', '(Monete_que_no_escucha@lostresmonetes.co.uk).']</code></pre>

Vaya, entre los resultados se nos han colado cosas que no serían direcciones de correo (los tres últimos elementos de la lista). Vamos a intentar solucionarlo usando un patrón un poco más complejo.

El patrón propuesto ahora sería algo como lo siguiente: `'w+@w+'`

donde

`'w'` encuentra cualquier caracter que sea alfanumérico (todas las letras mayúsculas y minúsculas, los números y el símbolo `'_'`). Esto sería equivalente a usar `r'[a-zA-Z0-9_]'`

`'+'` indica que hay que encontrar al menos un caracter que no sea un espacio en blanco

`'@'` indica la arroba

<pre><code class="language-python">print(re.findall('w+@w+',texto))</code></pre>

La salida del anterior código mostrará:

<pre><code class="language-python">['monete_que_no_ve@lostresmonetes', 'torpedo@submarino', 'torpedo@submarino', 'monete_que_no_ve@lostresmonetes', 'monete_que_no_ve@lostresmonetes', 'torpedo@submarino', 'torpedo@submarino', 'monete_que_no_ve@lostresmonetes', 'monete_que_no_ve@lostresmonetes', 'torpedo@submarino', 'habla@lostresmonetes', 'w@pa', 'Monete_que_no_escucha@lostresmonetes']</code></pre>

Ups, vaya, como hemos usado 'w' se han perdido las terminaciones de las direcciones de correo a continuación del símbolo '.' ('.net', '.com', '.co.uk') ya que no está incluido en la búsqueda. También vemos que hemos extraído incorrectamente una de las direcciones de correo que usa '.' antes de la '@' ('Monete.que.no.habla@lostresmonetes.net')

Vamos a volver a probar con un patrón diferente: `r'w+[.]*@w+[.]*w+'`

donde:

`'w'` encuentra cualquier caracter que sea alfanumérico (todas las letras mayúsculas y minúsculas, los números y el símbolo `'_'`). Esto sería equivalente a usar [a-zA-Z0-9]

`'[.]'` incluye el símbolo `'.'` dentro del patrón a buscar. Sería equivalente a usar `r'[a-zA-Z0-9_.]'`

`'+'` indica que hay que encontrar al menos un caracter que no sea un espacio en blanco

`'@'` indica la arroba

<pre><code class="language-python">print(re.findall(r'w+[.]*@w+[.]*w+', texto))</code></pre>

La salida del anterior código mostrará:

<pre><code class="language-python">['monete_que_no_ve@lostresmonetes.net', 'torpedo@submarino.com', 'torpedo@submarino.com', 'monete_que_no_ve@lostresmonetes.net', 'monete_que_no_ve@lostresmonetes.net', 'torpedo@submarino.com', 'torpedo@submarino.com', 'monete_que_no_ve@lostresmonetes.net', 'monete_que_no_ve@lostresmonetes.net', 'torpedo@submarino.com', 'habla@lostresmonetes.net', 'w@pa', 'Monete_que_no_escucha@lostresmonetes.co']</code></pre>

Vaya. Hemos recuperados las terminaciones del _host_ ('.net', '.com') pero no hemos recuperado correctamente la dirección de correo errónea ni la dirección del correo con terminación '.co.uk'... ¿Qué podemos hacer? Pues probar con otro patrón que haga lo que necesitamos.

El patrón propuesto ahora sería: `r'[w.]*@[w.]*'`

donde

'[w.]*' busca cualquier cosa que contenga una letra (desde la _a_ la _z_ en mayúsculas o minúsculas), un número, el símbolo `'_'` y/o el símbolo `'.'`

`'@'` indica la arroba

<pre><code class="language-python">print(re.findall(r'[w.]*@[w.]*', texto))</code></pre>

La salida del anterior código mostrará:

<pre><code class="language-python">['monete_que_no_ve@lostresmonetes.net', 'torpedo@submarino.com', 'torpedo@submarino.com', 'monete_que_no_ve@lostresmonetes.net', 'monete_que_no_ve@lostresmonetes.net', 'torpedo@submarino.com', 'torpedo@submarino.com', 'monete_que_no_ve@lostresmonetes.net', 'monete_que_no_ve@lostresmonetes.net', 'torpedo@submarino.com', 'Monete.que.no.habla@lostresmonetes.net', 'w@pa', 'Monete_que_no_escucha@lostresmonetes.co.uk']</code></pre>

Maldición, se nos ha seguido colando una cosa que no es una dirección de correo. Podría eliminarla pidiéndo que después de la arroba deba figurar al menos un símbolo `'.'`.

Nuevo patrón: `r'[w.]*@w*.[w.]*'`

donde

`'[w.]*'` busca cualquier cosa que contenga una letra (desde la a la z en mayúsculas o minúsculas), un número, el símbolo `'_'` y/o el símbolo `'.'`

`'@'` indica la arroba

`'w+.[w.]*'` primero busca cualquier cosa que contenga al menos una letra (desde la a la z en mayúsculas o minúsculas), un número y/o el símbolo `'_'`, segundo, exige que haya un punto y, por último, vuelve a buscar cualquier cosa que contenga una letra (desde la a la z en mayúsculas o minúsculas), un número, el símbolo `'_'` y/o el símbolo `'.'`. Es decir, este último subpatrón encontraría cosas como por ejemplo 'hola.com', 'hola.co.uk', 'hola\_.com', 'hola.co\_m',..., que no tienen que ser correctas como dominio o 'host' pero que permiten filtrar a 'w@pa'

<pre><code class="language-python">print(re.findall(r'[w.]*@w+.[w.]*', texto))</code></pre>

La salida del anterior código mostrará:

<pre><code class="language-python">['monete_que_no_ve@lostresmonetes.net', 'torpedo@submarino.com', 'torpedo@submarino.com', 'monete_que_no_ve@lostresmonetes.net', 'monete_que_no_ve@lostresmonetes.net', 'torpedo@submarino.com', 'torpedo@submarino.com', 'monete_que_no_ve@lostresmonetes.net', 'monete_que_no_ve@lostresmonetes.net', 'torpedo@submarino.com', 'Monete.que.no.habla@lostresmonetes.net', 'Monete_que_no_escucha@lostresmonetes.co.uk']</code></pre>

Qué pasa si, por la razón que sea, queremos obtener el usuario del correo y el dominio por separado para ¡lo que sea que se te ocurra! Ha llegado el momento de introducir los grupos. Los grupos son patrones o subpatrones encerrados entre paréntesis.

Podemos proponer el siguiente patrón y ver qué pasa: `r'([w.]*)@(w+.[w.]*)'`

Este patrón es el mismo que el de antes pero encerrando lo que queremos que sea un grupo entre paréntesis.

Para el siguiente ejemplo vamos a usar la función [_finditer_](http://docs.python.org/3.3/library/re.html#re.finditer) en lugar de la función [_findall_](http://docs.python.org/3.3/library/re.html#re.findall), ambas del módulo [_re_](http://docs.python.org/3.3/library/re.html).

<pre><code class="language-python">iterador = re.finditer(r'([w.]*)@(w+.[w.]*)', texto)
users = []
hosts = []
for tupla in iterador:
    users.append(tupla.group(1))
    hosts.append(tupla.group(2))
print('Nos han escrito:')
for user in set(users): print('  ' + user)
print('desde los siguientes dominios')
for host in set(hosts): print('  ' + host)</code></pre>

La salida del anterior código mostrará:

<pre><code class="language-python">Nos han escrito:
  torpedo
  Monete.que.no.habla
  Monete_que_no_escucha
  monete_que_no_ve
desde los siguientes dominios
  submarino.com
  lostresmonetes.net
  lostresmonetes.co.uk</code></pre>

El iterador devuelve un [objeto Match](http://docs.python.org/3.3/library/re.html#match-objects), que es una clase con sus métodos y sus cosicas. El método _group_ nos devolverá el elemento del grupo que le pidamos. En este caso se usaría el índice _1_ para el primer grupo, _2_ para el segundo y __ o nada para que nos devuelva todo lo encontrado con el patrón usado, es decir, lo mismo que si no hubiéramos usado grupos.

En este caso solo se usan dos grupos en el patrón pero podría darse el caso de que el patrón se volviese más complejo y nos interesase incluir más grupos. Para evitar liarnos podríamos usar nombres para los grupos de la siguiente manera:

Patrón: `r'(?P<users>[w.]*)@(?P<hosts>w+.[w.]*)'`

donde

`'?P<nombre_del_grupo>'` es la forma de identificar el grupo con `nombre_del_grupo` siendo el valor que quieras usar para nombrar a ese determinado grupo.

En la pieza de código siguiente deberéis reemplazar en la primera línea `patron` por `r'(?P<users>[w.]*)@(?P<hosts>w+.[w.]*)'`. Disculpad las molestias pero wordpress.com 'escapa' algunas cosas del código.

<pre><code class="language-python">iterador = re.finditer(patron, texto)
hosts = []
users = []
for tupla in iterador:
    users.append(tupla.group('users'))
    hosts.append(tupla.group('hosts'))
print('Nos han escrito:')
for user in set(users): print('  ' + user)
print('desde los siguientes dominios')
for host in set(hosts): print('  ' + host)</code></pre>

La salida del anterior código mostrará:

<pre><code class="language-python">Nos han escrito:
  torpedo
  Monete.que.no.habla
  Monete_que_no_escucha
  monete_que_no_ve
desde los siguientes dominios
  submarino.com
  lostresmonetes.net
  lostresmonetes.co.uk</code></pre>

Ahora queremos sustituir la dirección del usuario por otro patrón para así ocultar sus direcciones. Eso lo podemos hacer mediante las funciones [_sub_](http://docs.python.org/3.3/library/re.html#re.sub) o [_subn_](http://docs.python.org/3.3/library/re.html#re.subn) de la siguiente forma.

En la pieza de código siguiente deberéis reemplazar en la primera línea `patron` por `r'(?P<users>[w.]*)@(?P<hosts>w+.[w.]*)'` y `patron2` por `r'----------@g<hosts>'`. Disculpad las molestias pero wordpress.com 'escapa' algunas cosas del código.

<pre><code class="language-python">print(re.sub(patron, patron2, texto))</code></pre>

La salida del anterior código mostrará:

<pre><code class="language-python">De: ----------@lostresmonetes.net
Enviado el: Jueves, 18 de noviembre de 2012 a las 13:22
Para: ----------@submarino.com
Asunto: Re: Conquistar el mundo
Hola.
Aapfojewagf ajwa wjepofoisa jvgoisajigf jewapoijewagomsod moisjaoigjpoewijsn dsanigeaoi.
Ajfpoijwafe sodvm osznfinewahaw eoansjgndsakjnglkjds.
Alkjndszkng aigpiewannalkjndkjnlkjdznvns ln sa nfpoiewa npoinpewnpofn.
N&lt;sznvcknvknkxzvnoisajpoijewaoi jmsam lkvznapiunea engnal nfsl.
De: ----------@submarino.com
Enviado el: Jueves, 18 de noviembre de 2012 a las 12:42
Para: ----------@lostresmonetes.net
Asunto: Re: Conquistar el mundo
Hola.
Aapfojewagf ajwa wjepofoisa jvgoisajigf jewapoijewagomsod moisjaoigjpoewijsn dsanigeaoi.
Ajfpoijwafe sodvm osznfinewahaw eoansjgndsakjnglkjds.
Alkjndszkng aigpiewannalkjndkjnlkjdznvns ln sa nfpoiewa npoinpewnpofn.
N&lt;sznvcknvknkxzvnoisajpoijewaoi jmsam lkvznapiunea engnal nfsl.
De: ----------@lostresmonetes.net
Enviado el: Jueves, 18 de noviembre de 2012 a las 11:57
Para: ----------@submarino.com
Asunto: Re: Conquistar el mundo
Hola.
Aapfojewagf ajwa wjepofoisa jvgoisajigf jewapoijewagomsod moisjaoigjpoewijsn dsanigeaoi.
Ajfpoijwafe sodvm osznfinewahaw eoansjgndsakjnglkjds.
Alkjndszkng aigpiewannalkjndkjnlkjdznvns ln sa nfpoiewa npoinpewnpofn.
N&lt;sznvcknvknkxzvnoisajpoijewaoi jmsam lkvznapiunea engnal nfsl.
De: ----------@submarino.com
Enviado el: Jueves, 18 de noviembre de 2012 a las 11:54
Para: ----------@lostresmonetes.net
Asunto: Re: Conquistar el mundo
Hola.
Aapfojewagf ajwa wjepofoisa jvgoisajigf jewapoijewagomsod moisjaoigjpoewijsn dsanigeaoi.
Ajfpoijwafe sodvm osznfinewahaw eoansjgndsakjnglkjds.
Alkjndszkng aigpiewannalkjndkjnlkjdznvns ln sa nfpoiewa npoinpewnpofn.
N&lt;sznvcknvknkxzvnoisajpoijewaoi jmsam lkvznapiunea engnal nfsl.
De: ----------@lostresmonetes.net
Enviado el: Jueves, 18 de noviembre de 2012 a las 09:15
Para: ----------@submarino.com
Asunto: Conquistar el mundo
Hola.
Aapfojew mi primo el monete que no habla (----------@lostresmonetes.net) agf ajwa wjepofoisa jvgoisajigf.
Para la ninia + w@pa del tuenti, hoygan (----------@lostresmonetes.co.uk).
Ajfpoijwafe sodvm osznfinewahaw eoansjgndsakjnglkjds.
Alkjndszkng aigpiewannalkjndkjnlkjdznvns ln sa nfpoiewa npoinpewnpofn.
N&lt;sznvcknvknkxzvnoisajpoijewaoi jmsam lkvznapiunea engnal nfsl.</code></pre>

Y, de momento, ya vale. Solo hemos rascado un poco pero espero que os haya valido de algo. Si encuentro tiempo habrá un capítulo II con más ejemplos para que este tutorial o lo que sea que haya salido se amplíe con cosas más complejas (a medida que tenga más soltura con ello).

Si queréis seguir por vuestra cuenta podéis usar:

[La documentación oficial del módulo re](http://docs.python.org/3.3/library/re.html)

[El HOW-TO de la documentación oficial](http://docs.python.org/2/howto/regex.html)

[Expresiones regulares en Google-developers](https://developers.google.com/edu/python/regular-expressions)

[La aplicación de escritorio KODOS](http://kodos.sourceforge.net/) o una [versión online](http://www.pythonregex.com/) de la misma herramienta.

[Algún completo libro sobre expresiones regulares](http://www.amazon.com/s/ref=nb_sb_noss_1?url=search-alias%3Dstripbooks&field-keywords=regular%20expressions&sprefix=regular%2B%2Cstripbooks&rh=n:283155%2Ck%3Aregular%20expressions)

Saludos.

P.D.: Como siempre, se aceptan todo tipo de críticas constructivas y se agradecen todo tipo de correcciones a cosas incorrectas que haya dicho.

##### _This post has been published on wordpress.com from an ipython notebook using [ipynb2wp](https://github.com/kikocorreoso/ipynb2wp)_