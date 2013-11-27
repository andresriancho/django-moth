from django.shortcuts import render
from moth.views.base.vulnerable_template_view import VulnerableTemplateView


class EchoHeadersView(VulnerableTemplateView):
    description = title = 'Echoes all request headers'
    url_path = 'echo-headers.py'

    KNOWN_HEADERS = ('CONTENT_LENGTH',)

    def is_http_header(self, hname):
        return hname.startswith('HTTP_') or hname in self.KNOWN_HEADERS

    def translate_header(self, hname):
        hname = hname.replace('HTTP_', '')
        hname = hname.replace('_', '-')
        hname = hname.lower()
        hname = hname.title()
        return hname
        
    def get(self, request, *args, **kwds):
        context = self.get_context_data()
        
        html = ''
        msg_fmt = 'Header "%s" with value "%s" <br/>\n'
        
        for hname in request.META:
            if self.is_http_header(hname):
                html += msg_fmt % (self.translate_header(hname),
                                   request.META[hname])
            
        context['html'] = html
        
        return render(request, self.template_name, context)

