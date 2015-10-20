import StringIO
import logging
import gi
# suppress version warning from import
gi.require_version('Rsvg', '2.0')
from gi.repository import Rsvg as rsvg

from cairocontext import CairoContext

log = logging.getLogger('svg2pdf')

class Document:
    "document parameters and context"
    def __init__(self, response):
        self.output = 'output.pdf'
        self.width  = 0
        self.height = 0
        self.scalex = 1
        self.scaley = 1
        self.context = { 
            'res'    : response,
            'pages'  : 0,
            'cairo'  : None
        }

    def __setparam__(self, param, value):
        err = ''
        if hasattr(self, param) and param != 'context':
            log.debug("Set parameter: %s = %s" % (param, value))
            try:
                # dynamically cast to the type already in the attribute
                setattr(self, param, type(getattr(self,param))(value))
                return
            # type not compatible
            except (TypeError, ValueError) as e:
                err = ' type'
                pass
        log.error("Invalid parameter %s%s" % (param,err))
        
    def inc_page_count(self):
        self.context['pages'] += 1

    def page_count(self):
        return self.context['pages']

    # NOTE! Not form_from, but from_form! :-)
    def from_form(self, form):
        "Parses form-data parameters from POST request"
        for param in form:
            self.__setparam__(param, form[param])

    def from_json(self, file_upload):
        "Parses parameters from JSON"
        json = StringIO.StringIO()
        file_upload.save(json)
        self.from_form(yaml.safe_load(json))
    
    def render_page(self, svg_file):
        svg = rsvg.Handle.new()

        svg_file.save(svg)
        svg.close() # commit

        dims = svg.get_dimensions()
        self.set_context(dims.width, dims.height)
        log.debug(
            "Page: %d SVG: %sx%s" % 
            (self.page_count() + 1, dims.width, dims.height)
        )

        # Emit headers before the first page
        # they would be ignored afterwards
        if self.page_count() == 0:
            res = self.context['res']
            res.content_type = "application/pdf"
            res.add_header(
                'Content-Disposition',
                "attachment; filename=%s" % self.output
            )
        self.inc_page_count() 
        self.context['cairo'].render(svg)
        
    def set_context(self, w, h):
        width  = (self.width or w)  * self.scalex
        height = (self.height or h) * self.scaley
        if not self.context['cairo']:
            self.context['cairo'] = CairoContext(width, height)
        else:
            self.context['cairo'].set_size(width, height)
        
    def finish(self):
        return self.context['cairo'].finish()

    def flush(self):
        return self.context['cairo'].flush()

