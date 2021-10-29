TinyPreProcessor
================

This is a tiny pre processor with nearly cpp syntax.

Here an example:

```c
#include somefile.txt

#ifdef this-is-undefined
... will never happen...
#endif

#ifndef test1
#define test1
#include someother.txt
#endif

#define test2
#undef test2
```

Usage from python:

```py
from tinypreprocessor import TinyPreProcessor

def compile_something(filename):
    
    tpp = PreProcessor(suffix=".txt")
    tpp.load(filename)
    tmpfilename = tpp.done()
    
    with open(tmpfilename, "r") as f:
        pass # do stuff with tmpfilename
    
    # the temporary file will be deleted as soon
    # as the PreProcessor (tpp) object ist deleted

compile_something("example.txt")
```

Installation
------------

```sh
pip install git+https://github.com/maxdoom-com/tinypreprocessor
```
