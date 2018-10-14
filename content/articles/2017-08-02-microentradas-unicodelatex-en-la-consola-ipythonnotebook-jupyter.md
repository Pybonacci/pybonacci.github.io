Title: Microentradas: Unicode/látex en la consola IPython/notebook Jupyter
Date: 2017-08-02 19:17
Author: kiario
Category: Artículos
Tags: ipython, jupyter, látex, MicroEntradas, til, unicode
Slug: microentradas-unicodelatex-en-la-consola-ipythonnotebook-jupyter
Status: published

*Este es un [TIL](https://www.reddit.com/r/todayilearned/) que vi el
otro día. Lo dejo aquí por si otros no lo sabían y les resulta útil.*

En la consola de IPython o en el notebook Jupyter podéis usar unicode
escribiendo símbolos látex.

Por ejemplo, si escribes lo siguiente (en la consola o en una celda del
notebook):

    In [1]: \alpha

y pulsáis después la tecla `tab` veréis que se transforma a su símbolo
látex y lo podéis usar fácilmente en vuestro código.

El resultado sería algo como lo siguiente (antes y después de pulsar la
tecla `tab`):

-   Antes:

![console1](https://pybonacci.org/images/2017/08/console1.png?style=centerme)

-   Después:

![console2](https://pybonacci.org/images/2017/08/console2.png?style=centerme)

Esto puede ser útil para scripts propios, demos, formación,..., pero os
lo desaconsejo en código en producción o a compartir ;-)

Saludos.
