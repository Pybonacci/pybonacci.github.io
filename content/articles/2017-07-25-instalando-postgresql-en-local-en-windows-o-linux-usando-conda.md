Title: Instalando PostgreSQL en local en windows o linux usando conda
Date: 2017-07-25 18:49
Author: kiario
Category: Artículos, Tutoriales
Tags: base de datos, bases de datos, bbdd, conda, conda-forge, pgcli, postgresql, psycopg2
Slug: instalando-postgresql-en-local-en-windows-o-linux-usando-conda
Status: published

Para el que no lo sepa, podéis instalar PostgreSQL usando `conda` \\o/

Vamos a hacer un tutorial paso a paso para poder instalarlo todo y
dejarlo listo para trabajar desde Python de forma sencilla.

**\[*A lo largo de todo el tutorial se indica si el código a usar es
para windows o para linux. Si no se indica nada el código debería ser
válido en ambos sistemas operativos.*\]**

1. Creamos un entorno virtual usando `conda` e instalamos PostgreSQL.
=====================================================================

Este paso es sencillo. Solo necesitáis tener instalado `conda` en
vuestro equipo y una conexión a internet. Si no tenéis `conda` instalado
podéis ir a la sección de enlaces, más abajo, para visitar la
documentación de `conda` donde os indica como instalarlo. Con `conda`
instalado, podemos añadir el canal de `conda-forge` (básico para poder
extender la cantidad de paquetes disponibles además de los mantenidos
oficialmente). Lo podéis añadir a vuestros canales de referencia
mediante el siguiente código a ejecutar en la línea de comandos:

`conda config --add channels conda-forge`

Una vez hecho lo anterior, en vuestra línea de comandos, podéis
escribir:

`conda create --name pgenv postgresql python=3.6`

Lo anterior nos crea un entorno virtual `conda` llamado `pgenv` con
Python 3.6. Activamos el nuevo entorno que hemos creado escribiendo en
la línea de comandos:

`source activate pgenv` \# linux

`activate pgenv` \# windows

Antes de poder usar PostgreSQL debemos hacer alguna cosita más. Veamos
la siguiente sección.

2. Creando un cluster de BBDD
=============================

Una vez instalado PostgreSQL deberéis crear la carpeta de datos donde se
guardarán las BBDD (a esto se le llama cluster en los docs de
PostgreSQL).

Lo vamos a instalar en una carpeta que se llame ***data***. La carpeta
***data*** la creará el comando si no existe pero fallará si ya existe y
no está vacía. Por ello, para evitar problemas podemos crear la carpeta
a mano donde deseemos para asegurarnos que la misma esté vacía y para
asegurarnos que tenemos permisos de escritura en esa ubicación.

`mkdir /ruta/hasta/data` \# linux  
`mkdir "C:\\ruta\\hasta\\data"` \# windows.

En linux, ubicaciones populares de esta carpeta ***data*** son:

`/usr/local/pgsql/data`  
`/var/lib/pgsql/data`

Pero la podéis colocar donde queráis.

Y ahora vamos al comando en cuestión. Si estáis en linux podéis hacer:

`initdb -D /usr/local/pgsql/data` \# linux

En windows es similar pero con una ruta aceptable para windows:

`initdb -D "C:\\ruta\\hasta\\data"` \# windows

De forma alternativa podéis hacer:

`pg_ctl -D /usr/local/pgsql/data initdb` \# linux

`"pg_ctl" -D "C:\\ruta\\hasta\\data" initdb` \# windows

Es mejor usar, en general, `pg_ctl` ya que es el comando que usaremos
para arrancar, parar,..., el servidor de BBDD por lo que será útil
familiarizarnos con el mismo.

3. Arrancando el servidor de BBDD.
==================================

Podemos arrancar el servidor de BBDD usando:

`pg_ctl -D /usr/local/pgsql/data start` \# linux

`"pg_ctl" -D "C:\\ruta\\hasta\\data" start` \# windows

Si, además, queremos tener un fichero ***log*** con la información de lo
que se vaya  
haciendo podemos usar la opción `-l`:

`pg_ctl -D /usr/local/pgsql/data -l fichero_log start` \# linux

`"pg_ctl" -D "C:\\ruta\\hasta\\data" -l fichero_log start` \# windows

Y se creará un fichero de texto con la información llamado
***fichero\_log*** en la  
ubicación desde donde lanzamos el comando (o en la ruta que defináis si
así queréis). Es recomendable usar esta opción si no queréis que toda la
información se vaya mostrando en la línea de comandos y para tener un
registro de lo que vamos haciendo.

El directorio de datos se crea con seguridad mínima (modo ***trust***).
Como vamos a trabajar en local y, generalmente, en un sistema
monousuario o con usuarios en los que confiamos no vamos a prestar mucha
atención a esto pero puedes leer más sobre ello
[aquí](https://www.postgresql.org/docs/current/static/auth-methods.html).

El usuario por defecto del sistema que hace la instalación de PostgreSQL
(usando `conda` en este caso) es el que se puede usar para la base de
datos.

4. Interactuando con la base de datos.
======================================

Podemos instalar también `psycopg2`, driver para comunicar Python con
PostgreSQL, y `pgcli`, una línea de comandos con esteroides, lo que
viene a ser IPython para la consola Python. Con nuestro entorno `pgenv`
activado escribimos en la línea de comandos:

`conda install pgcli psycopg2`

Genial, ¡qué fácil todo!

Vamos a crear nuestra primera base de datos. Para ello deberemos tener
el servidor de BBDD funcionando. En este caso, con el comando que hemos
usado anteriormente, `pg_ctl ... start`, debería haber arrancado y lo
siguiente debería funcionar sin dar problemas:

`createdb dbtest`

Lo anterior debería haber creado una base de datos llamada ***dbtest***.
Si no ha  
habido ningún problema podríamos acceder con `pgcli` (o `psql`, el
comando de serie que viene con PostgreSQL) haciendo:

`pgcli dbtest` \# 'psql dbtest' en caso que no hayáis instalado pgcli

(si hemos entrado en `pgcli` o en `psql` podemos salir usando `\q`).

Ahora podríamos empezar a crear tablas e insertar datos pero, si os
acordáis, hemos instalado `psycopg2`. Usémoslo para hacerlo desde
Python.

El siguiente código va a crear una tabla llamada `tabla` y vamos a
insertar una serie de filas. Lo podéis ejecutar desde la consola Python
mismo:

``` {.language-python}
import psycopg2

# tu_usuario en la siguiente línea debería ser tu usuario del sistema
conn = psycopg2.connect("dbname=dbtest user=tu_usuario")

cur = conn.cursor()

cur.execute(
    "CREATE TABLE tabla (id serial PRIMARY KEY, num integer, num_txt varchar);"
)
cur.execute(
    "INSERT INTO tabla (num, num_txt) VALUES (%s, %s)", 
    (1, "uno")
)
cur.execute(
    "INSERT INTO tabla (num, num_txt) VALUES (%s, %s)",
    (10, "diez")
)

conn.commit()

cur.close()
conn.close()
```

Lo que hace el código anterior es, básicamente:

-   se conecta a la base de datos que acabamos de crear, ***dbtest***,
-   crea una tabla, llamada 'tabla',
-   mete varias filas de datos en esa nueva tabla y,
-   finalmente, cierra la conexión con la base de datos.

Desde la línea de comandos podemos usar `pgcli` para hacer una consulta,
también desde python pero vamos a hacerlo con `pgcli` en este caso:

(salid de la consola Python usando `exit()` si todavía estáis dentro de
la misma)

En la línea de comandos:

`pgcli dbtest` \# 'psql dbtest' si no habéis instalado pgcli

Ya dentro de `pgcli` (o `psql`) podemos hacer una consulta SQL:

``` {.language-sql}
SELECT * FROM tabla
```

Y nos debería dar el siguiente resultado:

    +------+-------+-----------+
    |  id  |  num  |  num_txt  |
    |------+-------+-----------|
    |   1  |   1   |    uno    |
    |   2  |   10  |    diez   |
    +------+-------+-----------+
    SELECT 2
    Time: 0.008s

Salimos nuevamente de `pgcli` (o `psql`) usando:

`\q`

5. Administración y limpieza.
=============================

Si no queréis la base de datos y la deseáis eliminar podéis usar, desde
la línea de comandos:

`dropdb dbtest`

Y la base de datos se borrará.

Vamos a apagar el servidor PostgreSQL para ver como se hace:

`pg_ctl -D /usr/local/pgsql/data stop` \# linux

`"pg_ctl" -D "C:\\ruta\\hasta\\data" stop` \# windows

Si lo quisiéramos volver a arrancar podemos hacer:

`pg_ctl -D /usr/local/pgsql/data start` \# linux

`"pg_ctl" -D "C:\\ruta\\hasta\\data" start` \# windows

Podéis ver las diferentes opciones del comando `pg_ctl` mediante:

`pg_ctl --help`

Y eso es todo. Una forma sencilla de usar PostgreSQL en local mediante
`conda`.

6. Eliminar el entorno virtual y PostgreSQL de forma eficaz.
============================================================

Eliminarlo todo sería tan sencillo como eliminar el entorno `conda`
creado una vez que lo tengamos desactivado y que el servidor de BBDD
este parado.

Para parar el servidor de BBDD hacemos en la línea de comandos:

`pg_ctl -D /usr/local/pgsql/data stop` \# linux

`"pg_ctl" -D "C:\\ruta\\hasta\\data" stop` \# windows

Para desactivar el entorno virtual hacemos desde la línea de comandos

`source deactivate` \# linux

`deactivate` \# windows

Y para borrar el entorno virtual `pgenv` hacemos, desde la línea de
comandos:

`conda-env remove --name pgenv`

Si, además, queremos hacer limpieza general de `conda`, limpiar paquetes
'cacheados' y liberar espacio en disco podemos hacer desde la linea de
comandos:

`conda clean -pt`

Finalmente, borramos la carpeta ***data*** que creamos al principio de
esta entrada.

`rm -fr /usr/local/pgsql/data` \# linux

`rmdir "C:\\ruta\\hasta\\data" /s /q` \# windows

Enlaces.
========

Página oficial de Postgresql: <https://www.postgresql.org/>  
Documentación oficial de Postgresql: <https://www.postgresql.org/docs/>  
Documentación oficial de conda: <https://conda.io/docs/>  
Por si queréis cambiar el usuario y/o password que usa conda en la
instalación:
<https://stackoverflow.com/questions/15008204/how-to-check-postgres-user-and-password#15008311>  
Documentación oficial de psycopg2:
<http://initd.org/psycopg/docs/index.html>  
Página oficial de pgcli: <https://www.pgcli.com/>

Notas finales.
==============

No se entra en profundidad en ninguna de las herramientas (PostgreSQL,
pgcli, psycopg2) para mantener el tutorial lo más sencillo posible.

En los enlaces tenéis mucha más información para ampliar.

En ningún caso se presta atención al tema de seguridad, configuración en
profundidad,..., de PostgreSQL ya que eso daría para unas cuantas
entradas.

¡¡Disfruten lo instalado!!
