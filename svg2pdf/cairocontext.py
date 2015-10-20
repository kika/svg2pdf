import yaml # Using PyYAML instead of JSON to get rid of Unicode keys
import cairo

from io import BytesIO
import logging

log = logging.getLogger('svg2pdf')

class CairoContext:
    def __init__(self, width, height):
        self.outbuf  = BytesIO()
        self.surface = cairo.PDFSurface(self.outbuf, width, height)
        self.context = cairo.Context(self.surface)

    def set_size(self, w, h):
        self.surface.set_size(w, h)

    def render(self, svg):
        if not svg.render_cairo(self.context):
            log.critical("SVG failed to render")
        else:
            # flush the page to the drawing surface
            self.surface.show_page()

    def finish(self):
        "Closes the drawing surface and pushes the last data out"
        self.surface.finish()
        return self.flush()

    def flush(self):
        "Returns data from the buffer and resets buffer to 0"
        out = self.outbuf.getvalue()
        self.outbuf.seek(0)
        self.outbuf.truncate(0)
        return out



