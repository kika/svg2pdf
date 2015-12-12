# SVG to PDF rendering microservice

Written in Python (tested on 2.7.10) using LibRSVG for SVG parsing and Cairo for actual rendering.

Only ~5% slower than similar implementation in pure C.

Expects `multipart/form-data` as input to the `/process` POST request and streams `application/pdf` back. Doesn't include any authentication and data validation.

Supports multipage rendering. Supports SVGs with embedded SVGs and with embedded Data-URI encoded images.

Parameters accepted, either as form-data parameters or JSON key/values:

Name | Description | Default
-----|-------------|--------
`width`,`height`  | Dimensions of the output page(s) in points. If not specified, or set to  zero, then dimensions from the SVG file are taken. If there are multiple SVG files, then every page may have a different size. If these parameters are specified all pages have the same size. | `0`
`scalex` | Float value, scale of the width. Width of the page would be multiplied by this number. | `1.0`
`scaley` | Float value, scale of the height. Height of the page would be multiplied by this number. | `1.0`
`output`| Name of the fictitious "output file". Parameter that would be returned in the `Content-Disposition` header. | `output.pdf`

You can supply these parameters as form inputs or as JSON file, sent as file upload, or both. You can even have multiple JSON files sent among SVG pages and parameters, specified in each file would be effective starting from the page following this parameter file upload.

SVG file(s) are "attached" to the request as file uploads with type `application/svg+xml`.

Output stream is flushed after each page.

### Dependencies:

* PyCairo
* PyGObject
* PyYAML
* Bottle

On OS X:
    `brew install pygobject3`
    It will bring both PyGObject and PyCairo
On Linux:
    `yum install pycairo librsvg2 pygobject3`
