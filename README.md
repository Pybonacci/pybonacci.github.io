# Source for http://pybonacci.github.io

This repository contains the source for http://pybonacci.github.io/.

_Based on the wonderful job by Jake Vanderplas https://github.com/jakevdp/jakevdp.github.io-source (MIT License)_

## Building the Blog

Clone the repository & make sure submodules are included

```
$ git clone https://github.com/Juanlu001/pybonacci.github.io-source.git
$ git submodule update --init --recursive
```

Install the required packages:

```
$ conda env create [ -f environment.yml ]
$ source activate pybonacci36
$ npm install -g less
```

Build the html and serve locally:

```
$ make html
$ make serve
$ open http://localhost:8000
```

Deploy to github pages

```
$ make publish-to-github
```

