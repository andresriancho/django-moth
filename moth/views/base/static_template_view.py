import mimetypes
import os

from django.http import HttpResponse
from moth.views.base.vulnerable_template_view import VulnerableTemplateView


STATIC_DIR = 'moth/static/moth/misc/'


class StaticFileView(VulnerableTemplateView):
    '''
    When we want to return the content of a static file, which doesn't
    make sense to store inside the .py source file, then we use this nice
    wrapper to do so.
    
    Files are read from the moth/static/misc/ directory.
    '''
    STATIC_FILE = None
    
    def get(self, request, *args, **kwds):
        if self.STATIC_FILE is None:
            raise RuntimeError('STATIC_FILE needs to be set.')

        file_path = os.path.join(STATIC_DIR, self.STATIC_FILE)
        content_type, _ = mimetypes.guess_type(self.STATIC_FILE)
        
        return HttpResponse(file(file_path).read(),
                            content_type=content_type)
