---
title: Hoy celebramos nuestro artículo número&#8230;
date: 2012-11-04T22:32:34+00:00
author: Kiko Correoso
slug: hoy-celebramos-nuestro-articulo-numero

    :::python
    def fibo(n):
        if n == 0:
            return 0
        elif n == 1:
            return 1
        else:
            return fibo(n - 1) + fibo(n - 2)
    print u"Ya hemos llegado al artículo número ", fibo(10)