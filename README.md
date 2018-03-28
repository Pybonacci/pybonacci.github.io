# Código fuente de http://mmngreco.github.io

Éste repositorio contiene el código fuente de  http://mmngreco.github.io/.

_Estructura basada en el maravilloso trabajo de Jake Vanderplas en https://github.com/jakevdp/jakevdp.github.io-source (Licencia MIT) y Pybonacci en https://github.com/Pybonacci/pybonacci.github.io_
 
## Cómo generar el contenido del Blog

Para crear el contenido estático del blog se necesita tener instalado [conda](https://www.anaconda.com/download) y nodejs (que instalará el gestor de paquetes [npm](https://www.npmjs.com/))

1. Clona el repositorio y asegurate de que los submódulos están incluidos

```
$ git clone https://github.com/mmngreco/mmngreco.github.io.git
$ cd mmngreco.github.io.git
$ git submodule update --init --recursive
```

2. Instala los paquetes requeridos:

```
$ conda env create -f environment.yml
$ source activate mmngreco36
(mmngreco36) $ npm install -g less
```

3. Genera el archivo `main.css`:

```
(mmngreco36) $ lessc theme/templates/main.less > theme/templates/main.css
```

4. Genera el html estático y sirvelo localmente con `Pelican`:

```
(mmngreco36) $ make html
(mmngreco36) $ make serve
(mmngreco36) $ open http://localhost:8000
```

5. Despliega a Github Pages (requiere permisos de administrador).

```
(mmngreco36) $ make publish-to-github
```

