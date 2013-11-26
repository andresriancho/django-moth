from moth.views.base.vulnerable_template_view import VulnerableTemplateView
from django.shortcuts import render_to_response


HTML = 'Take a look at the Content-Security-Policy header.'
CSP_HEADER = 'Content-Security-Policy'


class CSPTemplateView(object):
    CSP = None
    
    def get(self, request, *args, **kwds):
        # pylint: disable=E1101
        context = self.get_context_data()
        context['html'] = HTML
        
        response = render_to_response(self.template_name, context)
        response[CSP_HEADER] = self.CSP
        
        return response

class CSPError1View(CSPTemplateView, VulnerableTemplateView):
    description = title = 'CSP header with error (1)'
    url_path = 'csp_with_error_1.html'
    CSP = 'default-src * ; script-src * ; object-src *'
    
class CSPError2View(CSPTemplateView, VulnerableTemplateView):
    description = title = 'CSP header with error (2)'
    url_path = 'csp_with_error_2.html'
    CSP = 'default-src *'
    
class CSPError3View(CSPTemplateView, VulnerableTemplateView):
    description = title = 'CSP header with error (3)'
    url_path = 'csp_with_error_3.html'
    CSP = 'def-src * ; sript-src toto.com ; default-src *'
    
class CSPView(CSPTemplateView, VulnerableTemplateView):
    description = title = 'Valid CSP header'
    url_path = 'csp_without_error.html'
    CSP = "default-src 'self' ; script-src 'self' ; script-nonce ABCDE"
    