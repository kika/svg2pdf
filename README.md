# SVG to PDF rendering microservice

Written in Python (tested on 2.7.10) using LibRSVG for SVG parsing and Cairo for actual rendering.

Only ~5% slower than similar implementation in pure C.

Expects `multipart/form-data` as input to the `/process` POST request and streams `application/pdf` back. Doesn't include any authentication and data validation.

### Dependencies:

* PyCairo
* PyGObject
* PyYAML
* Bottle

On OS X:
    `brew install pygobject3`
    It will bring both PyGObject and PyCairo
