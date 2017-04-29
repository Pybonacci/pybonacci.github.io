---
title: Palabras usadas en Python (palabras clave y <em>builtins</em>)
date: 2014-10-15T20:15:39+00:00
author: Kiko Correoso
slug: palabras-usadas-en-python-palabras-clave-y-builtins
tags: Ace, autocompletado, brython, pyschool, python, resaltado de sintaxis

Hace poco estuve incluyendo autocompletado de código Python3 en un editor online ([pyschool.net](http://pyschool.net/)) destinado a la educación que se está desarrollando dentro del [proyecto Brython](https://github.com/brython-dev/).

El editor online que se usa es [Ace](http://ace.c9.io/#nav=about) (el notebook de IPython usa [codemirror](http://codemirror.com/)). El modo Python de Ace incluye palabras de Python2 y Brython implementa Python3 por lo que el [resaltado de código y autocompletado oficial](https://github.com/ajaxorg/ace/blob/master/lib/ace/mode/python_highlight_rules.js#L42) incluido con Ace no se ajusta a lo que se quería usar en [pyschool.net](http://pyschool.net/). Para solventar esto creé el modo Python3 que se usa en el editor online (y que [próximamente también podréis ver y usar](https://github.com/brython-dev/brython/commit/538ca811490ae6370559aaf20da45db1b357115c) en el editor oficial en [Brython.info](http://brython.info/tests/editor.html)). Pero había que saber qué palabras incluir en el resaltado y autocompletado de Ace (ya estoy llegando a lo que quería mostrar). Y como Python es tan increible y tiene módulos para todo podéis hacer lo siguiente para obtener las palabras clave (_keywords_):

<pre class="language-python"><code class="language-python" data-language="python">import keyword
print(keyword.kwlist)</code></pre>

Que dará como resultado:

<pre class="language-python"><code class="language-python" data-language="python">['False', 'None', 'True', 'and', 'as', 'assert', 
'break', 'class', 'continue', 'def', 'del', 'elif', 
'else', 'except', 'finally', 'for', 'from', 'global', 
'if', 'import', 'in', 'is', 'lambda', 'nonlocal', 
'not', 'or', 'pass', 'raise', 'return', 'try', 
'while', 'with', 'yield']</code></pre>

Y podéis obtener las funciones integradas (_builtins_) usando:

<pre class="language-python"><code class="language-python" data-language="python">import builtins
print(dir(builtins))</code></pre>

Que dará como resultado:

<pre class="language-python"><code class="language-python" data-language="python">['ArithmeticError', 'AssertionError', 'AttributeError', 
'BaseException', 'BlockingIOError', 'BrokenPipeError', 'BufferError', 
'BytesWarning', 'ChildProcessError', 'ConnectionAbortedError', 'ConnectionError', 
'ConnectionRefusedError', 'ConnectionResetError', 'DeprecationWarning', 'EOFError', 
'Ellipsis', 'EnvironmentError', 'Exception', 'False', 'FileExistsError', 
'FileNotFoundError', 'FloatingPointError', 'FutureWarning', 'GeneratorExit', 
'IOError', 'ImportError', 'ImportWarning', 'IndentationError', 'IndexError',
'InterruptedError', 'IsADirectoryError', 'KeyError', 'KeyboardInterrupt', 
'LookupError', 'MemoryError', 'NameError', 'None', 'NotADirectoryError', 
'NotImplemented', 'NotImplementedError', 'OSError', 'OverflowError', 
'PendingDeprecationWarning', 'PermissionError', 'ProcessLookupError', 
'ReferenceError', 'ResourceWarning', 'RuntimeError', 'RuntimeWarning', 
'StopIteration', 'SyntaxError', 'SyntaxWarning', 'SystemError', 'SystemExit', 
'TabError', 'TimeoutError', 'True', 'TypeError', 'UnboundLocalError', 
'UnicodeDecodeError', 'UnicodeEncodeError', 'UnicodeError', 'UnicodeTranslateError', 
'UnicodeWarning', 'UserWarning', 'ValueError', 'Warning', 'ZeroDivisionError', 
'__build_class__', '__debug__', '__doc__', '__import__', '__loader__', '__name__', 
'__package__', '__spec__', 'abs', 'all', 'any', 'ascii', 'bin', 'bool', 'bytearray', 
'bytes', 'callable', 'chr', 'classmethod', 'compile', 'complex', 'copyright', 'credits', 
'delattr', 'dict', 'dir', 'divmod', 'enumerate', 'eval', 'exec', 'exit', 'filter', 
'float', 'format', 'frozenset', 'getattr', 'globals', 'hasattr', 'hash', 'help', 'hex', 
'id', 'input', 'int', 'isinstance', 'issubclass', 'iter', 'len', 'license', 'list', 
'locals', 'map', 'max', 'memoryview', 'min', 'next', 'object', 'oct', 'open', 'ord', 
'pow', 'print', 'property', 'quit', 'range', 'repr', 'reversed', 'round', 'set', 'setattr', 
'slice', 'sorted', 'staticmethod', 'str', 'sum', 'super', 'tuple', 'type', 'vars', 'zip']</code></pre>

Limpio, fácil, rápido. Es tan eficiente que me ha sobrado tiempo para escribir esta entrada!!!

Espero que a alguien le sirva en algún momento.

Saludos.

P.D.: Si alguien quiere incluir el modo Python3 que hemos incluido en Ace dentro de Brython lo puede encontrar [aquí](https://github.com/brython-dev/brython-in-the-classroom/blob/master/pyschool/static/js/ace/mode-python3.js).