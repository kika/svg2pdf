#!env python
from bottle import get, post, run, request, response

import timeit
import logging
import re

from svg2pdf.document import Document

log = logging.getLogger('svg2pdf')

# POST parameters:
#    output    : filename for the output (Content-Disposition) [output.pdf]
#    width     : dimensions for the output 
#    height    :    [0 = every page sized after the SVG file]
#    scalex    : scale for X [1.0]
#    scaley    : scale for Y [1.0]
# Parameters are passed either as form parameters or as JSON 'file' upload
#  in case of JSON it should come first in the list of files or unpredictable
#  results may occur. There could be multiple JSON files in the sequence of 
#  uploads each will override parameters from this point forward.
# The rest of the POST request is a series of 'application/svg+xml' file uploads
#  each of which is a separate page
# Returns either 'application/pdf' with the result on success or 
# appropriate error code (usually 500) on fatal error
@post('/process')
def process(): 
    if re.match("^multipart/form-data", request.get_header('Content-Type')):
        doc = Document(response)
        # If there are form parameters read them
        if len(request.forms):
            doc.from_form(request.forms)

        for name in request.files:
            f = request.files[name]
            if f.content_type == 'application/json':
                doc.from_json(f)
            elif f.content_type == 'application/svg+xml':
                t = timeit.default_timer()
                doc.render_page(f)
                log.info("Page render time: %f" % (timeit.default_timer() - t))
                yield doc.flush()
            else:
                log.warn("Non SVG/JSON input: %s -> %s" % (name, f.content_type))
        yield doc.finish()
        
if __name__ == '__main__':
    log.addHandler(logging.StreamHandler())
    log.setLevel(logging.DEBUG)
    run(host='localhost', port=8001, debug=False)
