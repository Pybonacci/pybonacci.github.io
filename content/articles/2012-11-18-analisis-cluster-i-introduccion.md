---
title: Análisis cluster (I): Introducción
date: 2012-11-18T21:39:39+00:00
author: Kiko Correoso
slug: analisis-cluster-i-introduccion
tags: agrupamiento clusters, ai, aprendizaje automático, aprendizaje no supervisado, artificial intelligence, clasificación clustering, ia, inteligencia artificial, machine learning, scipy.cluster, scipy.spatial, unsupervised learning

Vamos a empezar una mini-serie de artículos sobre clasificación no supervisada que dividiré, en principio, en tres capítulos. En este primer capítulo no vamos a ver nada de python (oooooohhhhh) pero creo que es necesario dividirlo así para no hacerlos excesivamente pesados y largos y para introducir un poco la teoría de forma muy somera. ¿Vamos al lío?

Una de las actividades más propias del ser humano consiste en clasificar ‘cosas’ en clases o categorías (¡¡nos encanta etiquetar!!). Esto nos permite simplificar la inmensa cantidad de información que nos está llegando en todo momento:

  * clase baja, media y alta
  * Líquido, sólido, gaseoso (y plasma, y condensado de Bosé-Einstein, y...)
  * Friki, flipado, raro, geek, normal,...
  * ...

A lo largo de todo el texto de esta mini-serie usaré términos tanto en español como en inglés puesto que, normalmente, la terminología anglosajona es también la más habitual en los textos en español.

**Brevísima introducción teórica**

El análisis cluster es el nombre genérico que recibe un tipo de procedimientos de aprendizaje NO supervisado (unsupervised learning) usados para crear clasificaciones o agrupaciones. De forma más detallada, se podría decir que consiste en procedimientos de clasificación no supervisada (no existe una información previa) sobre una muestra de ‘individuos’ que intenta reorganizarlos en grupos que pretenden ser homogéneos. Estos grupos son los que se conocen como ‘clusters’ y esta es la palabra que usaremos a lo largo del presente texto puesto que es la más ampliamente usada en la literatura tanto en inglés, obviamente, como en español.

<!--more-->

Como se ha comentado, en general, no se dispone de información previa sobre la posible estructura de las clases o categorías, solo se dispone de un conjunto de observaciones o medidas y se trata de asociar estas observaciones en grupos en los cuales hay alta ‘similitud’ entre los miembros del mismo grupo y baja ‘similitud’ con miembros de otros grupos. La palabra similitud la he dejado entrecomillada puesto que el significado de esta palabra dependerá del problema concreto.

Para poner en contexto el problema, se tiene que la cantidad de formas en que se pueden clasificar m observaciones en k grupos o clusters es un número de Stirling de segunda especie.

$S\_{m}^{(k)} = cfrac{1}{k!} sum\_{i=0}^{k} (-1)^{k-i} binom{k}{i} i^{m}$

Pero como, a priori, no conocemos el número de grupos óptimo para un problema concreto, tenemos que las posibles soluciones son suma de todos los números de Stirling, considerando desde un único grupo (k=1 y las m observaciones se agrupan en un único grupo) hasta el caso extremo donde hay tantos grupos como observaciones (k=m y cada observación es un grupo de un único miembro).

Así, para solo 25 observaciones tendríamos un número de posibilidades superior a $4 x 10^{18}$ ([qué bien se me da copiar!!!](http://www.ugr.es/~gallardo/pdf/cluster-1.pdf)).

**Tipos de análisis cluster que vamos a ver**

En esta mini-serie vamos a ver dos casos de clasificación no supervisada que son los más habituales aunque no son los únicos:

  * Clustering jerárquico (hierarchical clustering en inglés)
  * K-medias (k-means en inglés)

**¿Cuál será el problema que vamos a resolver?**

Imaginad que tengo series de temperatura a 2 metros por encima de la superficie terrestre de un modelo numérico de simulación atmosférica en una malla regular. Cada uno de estos nodos será una observación que contendrá simulaciones de la temperatura cada 6 horas, es decir, cada una de estas observaciones será una serie temporal de datos de temperatura. Pero tengo un problema, quiero hacer un análisis de patrones de temperatura en todo Sudamérica y esto representa un montón de nodos (observaciones). ¿Puedo simplificar mi análisis agrupando estas series para usar solo una de cada grupo como representativa del grupo y así solo analizar k 'individuos' en lugar de m 'series' (siendo k<m)?

**Anotaciones finales**

Hay que destacar que la interpretación de los resultados dependerá mucho del conocimiento del problema y de la habilidad y experiencia del usuario en este tipo de análisis (avisados estáis ;-)).

Y hasta aquí esta mini-introducción al problema que ni pretende ser exhaustiva ni rigurosa. Para obtener información introductoria más detallada se puede hacer uso del excelente texto que he encontrado en [este enlace de la universidad de Granada (apuntes de José Ángel Gallardo San Salvador).](http://www.ugr.es/~gallardo/pdf/cluster-1.pdf)

**Miscelánea**

Os he dicho que no íbamos a ver python, os he mentido, vamos a ver un poco de (monty) python:

{% youtube i3v-nEy1Fzk %}

Hasta el siguiente capítulo de la mini-serie.
