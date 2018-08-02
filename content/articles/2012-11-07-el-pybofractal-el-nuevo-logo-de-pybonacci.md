---
title: El Pybofractal, el nuevo logo de Pybonacci
date: 2012-11-07T10:32:17+00:00
author: Juan Luis Cano
slug: el-pybofractal-el-nuevo-logo-de-pybonacci
tags: fibonacci, fractales, logo, pybonacci, python

El otro día estaba yo en el Twitter de Pybonacci para variar, y se me ocurrió que tal vez la imagen que representaba al blog en aquel momento, aunque había valido para salir del paso unos meses, no era demasiado significativa y que necesitábamos un cambio:

<blockquote class="twitter-tweet" width="550">
  <p>
    ¿Quién más piensa que necesitamos un logo con un poco más de personalidad? =)
  </p>
  
  <p>
    &mdash; Pybonacci (@Pybonacci) <a href="https://twitter.com/Pybonacci/statuses/251580091757387776">September 28, 2012</a>
  </p>
</blockquote>



Algunas personas se interesaron y Kiko sugirió entonces usar fractales, concretamente una **rosa de Fibonacci**:

<blockquote class="twitter-tweet" width="550">
  <p>
    <a href="https://twitter.com/Pybonacci">@Pybonacci</a> <a href="https://twitter.com/python_majibu">@python_majibu</a> <a href="https://twitter.com/nessa_los">@nessa_los</a> [k] un fractal de fibonacci <a href="http://t.co/viWGKLii">http://t.co/viWGKLii</a> <a href="http://t.co/CvPaR8Mu">http://t.co/CvPaR8Mu</a>
  </p>
  
  <p>
    &mdash; Pybonacci (@Pybonacci) <a href="https://twitter.com/Pybonacci/statuses/251707454637883392">September 28, 2012</a>
  </p>
</blockquote>



Ayer vi en los borradores del blog que había vuelto a rescatar el tema, y dije: ¡esta es mi oportunidad! Así que después de un par de iteraciones, Kiko dio con una idea genial: ¿por qué no generar el logo de Pybonacci con un script Python? 🙂 ¡Y eso es lo que hicimos!

Os presentamos al **Pybofractal**, **el nuevo logo de Pybonacci**:<figure id="attachment_1205" style="width: 440px" class="wp-caption aligncenter">

[<img class=" wp-image-1205 " title="Pybofractal" alt="" src="http://new.pybonacci.org/images/2012/11/pybofractal1.png" height="440" width="440" srcset="https://pybonacci.org/wp-content/uploads/2012/11/pybofractal1.png 550w, https://pybonacci.org/wp-content/uploads/2012/11/pybofractal1-150x150.png 150w, https://pybonacci.org/wp-content/uploads/2012/11/pybofractal1-300x300.png 300w" sizes="(max-width: 440px) 100vw, 440px" />](http://new.pybonacci.org/images/2012/11/pybofractal1.png)<figcaption class="wp-caption-text">El Pybofractal, el nuevo logo de Pybonacci</figcaption></figure> 

<!--more-->

Y este es el código que utilizamos para generarlo. Kiko es el autor principal, yo solo me encargué de los colores 😉

    :::python
    # coding: utf-8
    #
    # Script Python para generar el Pybofractal.
    # Autor: Kiko Correoso
    # Colores y acomodación a PEP8 por Juan Luis Cano
    import numpy as np
    from matplotlib import pyplot as plt
    def pybofractal(pto, lado, iteraciones, ax):
        """Genera el Pybofractal, el logo de Pybonacci.
        """
        colors = ['#39719e', '#3d79aa', '#4385bb', '#5390c1',
                '#70a4cb', '#ffe771', '#ffd333', '#ffcf23']
        ax.axis('off')
        punto1 = pto
        punto2 = (punto1[0] + lado * np.cos(np.deg2rad(60)),
        punto1[1] + lado * np.sin(np.deg2rad(60)))
        punto3 = (punto1[0] + lado, punto1[1])
        ax.fill((punto1[0], punto2[0], punto3[0], punto1[0]),
                (punto1[1], punto2[1], punto3[1], punto1[1]),
                edgecolor="w", linewidth=2.0, facecolor=colors[0])
        def cambio_coord((x, y), (x0, y0), i):
            x1 = ((x - x0) * np.cos(np.deg2rad(360 - (i * 60))) -
                 (y - y0) * np.sin(np.deg2rad(360 - (i * 60)))) + x0
            y1 = ((x - x0) * np.sin(np.deg2rad(360 - (i * 60))) +
                 (y - y0) * np.cos(np.deg2rad(360 - (i * 60)))) + y0
            return (x1, y1)
        for i in range(1, iteraciones):
            punto1 = punto2
            punto2 = (punto1[0] + lado * np.cos(np.deg2rad(60)) / ((2. / 3) ** i),
                    punto1[1] + lado * np.sin(np.deg2rad(60)) / ((2. / 3) ** i))
            punto3 = (punto1[0] + lado / ((2. / 3) ** i), punto1[1])
            punto2 = cambio_coord(punto2, punto1, i)
            punto3 = cambio_coord(punto3, punto1, i)
            ax.fill((punto1[0], punto2[0], punto3[0], punto1[0]),
                    (punto1[1], punto2[1], punto3[1], punto1[1]),
                    edgecolor="w", linewidth=2.0 + 0.618 * i, facecolor=colors[i])
    fig = plt.figure(figsize=(6, 6))
    ax = fig.add_subplot(111)
    ax.set_aspect(1)
    pybofractal((0, 0), 1, 7, ax)
    plt.savefig('pybofractal.svg')

Esperemos que os guste, ¡un saludo a todos!