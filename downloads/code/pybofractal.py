# Script Python para generar el Pybofractal.
# Autor: Kiko Correoso
# Colores y acomodación a PEP8 por Juan Luis Cano

import numpy as np
from matplotlib import pyplot as plt


def cambio_coord(p, p0, i):
    x, y = p
    x0, y0 = p0
    x1 = ((x - x0) * np.cos(np.deg2rad(360 - (i * 60))) -
         (y - y0) * np.sin(np.deg2rad(360 - (i * 60)))) + x0
    y1 = ((x - x0) * np.sin(np.deg2rad(360 - (i * 60))) +
         (y - y0) * np.cos(np.deg2rad(360 - (i * 60)))) + y0
    return (x1, y1)


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
