from moth.views.base.vulnerable_template_view import VulnerableTemplateView
from django.shortcuts import render


class HTMLTemplateView(VulnerableTemplateView):
    '''
    All vulnerabilities inherit from this template, which will render the data
    returned by the subclasses, disable anti-CSRF, etc.
    '''
    # If the subclass just wants to return static HTML, we give him a shortcut
    # where he doesn't define the get method, just sets HTML and we'll do the
    # rest
    HTML = None

    def get(self, request, *args, **kwds):
        if self.HTML is None:
            raise RuntimeError('HTML needs to be set.')
        
        context = self.get_context_data()
        context['html'] = self.HTML

        response = render(request, self.template_name, context)

        for key, value in self.extra_headers.iteritems():
            response[key] = value

        return response
