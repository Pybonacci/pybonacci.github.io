---
title: Joyitas en la stdlib: pathlib
date: 2016-05-18T22:06:30+00:00
author: Kiko Correoso
slug: joyitas-en-la-stdlib-pathlib
tags: directorios, ficheros, path, pathlib, rutas, stdlib

El otro día estuvimos hablando de la [biblioteca `collections`](http://pybonacci.org/2016/05/08/joyitas-en-la-stdlib-collections/), una joya dentro de la librería estándar. Hoy vamos a hablar de una nueva biblioteca que se incluyó en la versión 3.4 de CPython llamada [`pathlib`](https://docs.python.org/3/library/pathlib.html).

**Solo python 3, actualízate!!!**

Esta biblioteca nos da la posibilidad de usar clases para trabajar con las rutas del sistema de ficheros con una serie de métodos muy interesantes.

# Algunas utilidades para configurar el problema

Vamos a crear un par de funciones que nos permiten crear y borrar un directorio de pruebas para poder reproducir el ejemplo de forma sencilla:

    :::python
    import os
    import glob
    import shutil
    from random import randint, choice, seed
    from string import ascii_letters

    # función que nos crea un directorio de prueba en
    # el mismo directorio del notebook
    def crea_directorio():
        seed(1)
        base = os.path.join(os.path.curdir,
                            'pybonacci_probando_pathlib')
        os.makedirs(base, exist_ok = True)

        for i in range(, randint(3, 5)):
            folder = ''.join([choice(ascii_letters) for _ in range(4)])
            path = os.path.join(base, folder)
            os.makedirs(path, exist_ok = True)
            for j in range(, randint(2, 5)):
                ext = choice(['.txt', '.py', '.html'])
                name = ''.join([choice(ascii_letters) for _ in range(randint(5, 10))])
                filename = name + ext
                path2 = os.path.join(path, filename)
                open(path2, 'w').close()

    # Función que nos permite hacer limpieza 
    def borra_directorio():
        base = os.path.join(os.path.curdir,
                            'pybonacci_probando_pathlib')
        shutil.rmtree(base + os.path.sep)

Si ahora ejecutamos la función `crea_directorio`:

`crea\_directorio()`

Nos debería quedar una estructura parecida a lo siguiente:

    :::[]
    pybonacci_probando_pathlib/
    ├── KZWe
    │   ├── CrUZoLgubb.txt
    │   ├── IayRnBUbHo.txt
    │   ├── WCEPyYng.txt
    │   └── yBMWX.py
    ├── WCFJ
    │   ├── GBGQmtsLFG.html
    │   ├── PglOUshVv.py
    │   └── RoWDsb.py
    └── zLcE
        ├── AQlxJSXR.html
        ├── fCQGgXk.html
        └── xFUbEctT.html
    
Ejemplo usando lo disponible hasta hace poco
----------------------------------------------------------------------------------------------

Pensemos en un problema que consiste en identificar todos los ficheros _.py_ disponibles en determinada ruta y dejarlos en una nueva carpeta, que llamaremos _python_, todos juntos eliminándolos de la carpeta original en la que se encuentren.

De la forma antigua esto podría ser así:

    :::python
    # Suponemos que ya has creado los directorios y ficheros
    # de prueba usando crea_directorio()

    # recolectamos todos los ficheros *.py con sus rutas
    base = os.path.join(os.path.curdir,
                        'pybonacci_probando_pathlib')
    ficheros\_py = glob.glob(os.path.join(base, '**', '*.py'))

    # creamos la carpeta 'python' 
    # dentro de 'pybonacci_probando_pathlib'
    os.makedirs(os.path.join(base, 'python'), exist_ok = True)

    # y movemos los ficheros a la nueva carpeta 'python'
    for f in ficheros\_py:
        fich = f.split(os.path.sep)[-1]
        shutil.move(f, os.path.join(base, 'python'))

Nuestra nueva estructura de ficheros debería ser la siguiente:

    :::[]
    pybonacci_probando_pathlib/
    ├── KZWe
    │   ├── CrUZoLgubb.txt
    │   ├── IayRnBUbHo.txt
    │   └── WCEPyYng.txt
    ├── python
    │   ├── PglOUshVv.py
    │   ├── RoWDsb.py
    │   └── yBMWX.py
    ├── WCFJ
    │   └── GBGQmtsLFG.html
    └── zLcE
        ├── AQlxJSXR.html
        ├── fCQGgXk.html
        └── xFUbEctT.html

En el anterior ejemplo hemos tenido que usar las bibliotecas `glob`, `os` y `shutil` para poder realizar una operación relativamente sencilla. Esto no es del todo deseable porque he de conocer tres librerías diferentes y mi cabeza no da para tanto.

# Limpieza

Me cargo la carpeta _pybonacci\_probando\_pathlib_ para hacer un poco de limpieza:

`borra\_directorio()`

Y vuelvo a crear la estructura de ficheros inicial:

`crea_directorio()`

Después de la limpieza vamos a afrontar el problema usando `pathlib`.

El mismo ejemplo con `pathlib`

Primero importamos la librería y, como bonus, creamos una función que hace lo mismo que la función `borra_directorio` pero usando `pathlib`, que llamaremos `borra_directorio_pathlib`:

    :::python
    from pathlib import Path

    def borra_directorio_pathlib(path = None):
        if path is None:
            p = Path('.', 'pybonacci_probando_pathlib')
        else:
            p = path
        for i in p.iterdir():
            if i.is_dir():
                borra_directorio_pathlib(i)
            else:
                i.unlink()
        p.rmdir()

La anterior función con `shutil` es un poco más sencilla que con `pathlib`. Esto es lo único que hecho de menos en `pathlib`, algunas utilidades de `shutil` que vendrían muy bien de serie. Algo negativo tenía que tener.

En la anterior función, `borra_directorio_pathlib`, podemos ver ya algunas cositas de `pathlib`.

`p = Path('.', 'pybonacci_probando_pathlib')` nos crea una ruta que ahora es un objeto en lugar de una cadena. Dentro del bucle usamos el método [`iterdir`](https://docs.python.org/3/library/pathlib.html#pathlib.Path.iterdir) que nos permite iterar sobre los directorios de la ruta definida en el objeto `p`. el iterador nos devuelve nuevos objetos que disponen de métodos como [`is_dir`](https://docs.python.org/3/library/pathlib.html#pathlib.Path.is_dir), que nos permite saber si una ruta se refiere a un directorio, o [`unlink`](https://docs.python.org/3/library/pathlib.html#pathlib.Path.unlink), que nos permite eliminar el fichero o enlace. Por último, una vez que no tenemos ficheros dentro del directorio definido en `p` podemos usar el método [`rmdir`](https://docs.python.org/3/library/pathlib.html#pathlib.Path.rmdir) para eliminar la carpeta.

Ahora veamos cómo realizar lo mismo que antes usando `pathlib`, es decir, mover los ficheros _.py_ a la carpeta _python_ que hemos de crear.

    :::python
    # recolectamos todos los ficheros *.py con sus rutas
    p = Path('.', 'pybonacci_probando_pathlib')
    ficheros_py = p.glob('**\*.py')

    # creamos la carpeta 'python' dentro de 'pybonacci_probando_pathlib'
    (p  'python').mkdir(mode = 0o777, exist_ok = True)

    # y copiamos los ficheros a la nueva carpeta 'python'
    for f in ficheros_py:
        target = p / 'python' / f.name
        f.rename(target)

Nuevamente, nuestra estructura de ficheros debería ser la misma que antes:

    :::[]
    pybonacci_probando_pathlib/
    ├── KZWe
    │   ├── CrUZoLgubb.txt
    │   ├── IayRnBUbHo.txt
    │   └── WCEPyYng.txt
    ├── python
    │   ├── PglOUshVv.py
    │   ├── RoWDsb.py
    │   └── yBMWX.py
    ├── WCFJ
    │   └── GBGQmtsLFG.html
    └── zLcE
        ├── AQlxJSXR.html
        ├── fCQGgXk.html
        └── xFUbEctT.html
    
Repasemos el código anterior:  

Hemos creado un objeto ruta `p` tal como habíamos visto antes en la función `borra_directorio_pathlib`. Este objeto ahora dispone de un método [`glob`](https://docs.python.org/3/library/pathlib.html#pathlib.Path.glob) que nos devuelve un iterador con lo que le pidamos, en este caso, todos los ficheros con extensión _.py_. En la línea `(p / 'python').mkdir(mode = 0o777, exist_ok = True)` podemos ver el uso de `/` como operador para instancias de `Path`. El primer paréntesis nos devuelve una nueva instancia de `Path` que dispone del método [`mkdir`](https://docs.python.org/3/library/pathlib.html#pathlib.Path.mkdir) que hace lo que todos esperáis. Como `ficheros_py` era un iterador podemos usarlo en el bucle obteniendo nuevas instancias de `Path` con las rutas de los ficheros python que queremos mover. en la línea donde se define `target` hacemos uso del atributo [`name`](https://docs.python.org/3/library/pathlib.html#pathlib.PurePath.name),que nos devuelve la última parte de la ruta. Por último, el fichero con extensión _.py_ definido en el `Path` `f` lo renombramos a una nueva ruta, definida en `target`.

Y todo esto usando una única librería!!!

Echadle un ojo a la [documentación oficial](https://docs.python.org/3/library/pathlib.html) para descubrir otras cositas interesantes.

Si además de usar una única librería usamos parte de la funcionalidad de `shutil` tenemos una pareja muy potente, `pathlib` + `shutil`.

# Limpieza II

Y para terminar, limpiamos nuestra estructura de ficheros pero usando ahora la función `borra_directorio_pathlib` que habíamos creado pero no usado aún:

`borra_directorio_pathlib()`

# Notas

Ya hay un nuevo [PEP relacionado y aceptado](https://www.python.org/dev/peps/pep-0519/).

Enjoy!!
