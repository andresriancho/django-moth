from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render


class VulnerableTemplateView(TemplateView):
    '''
    All vulnerabilities inherit from this template, which will render the data
    returned by the subclasses, disable anti-CSRF, etc.
    '''
    # The template to use to render this view
    template_name = "moth/vulnerability.html"
    
    # The title that will appear on the rendered HTML
    title = None
    
    # The description that will appear on the rendered HTML
    description = None
    
    # The URL pattern string (not regex for now) which we'll try to match before
    # sending information to this view. This is parsed by the router view.
    url_path = None
    
    # If the subclass just wants to return static HTML, we give him a shortcut
    # where he doesn't define the get method, just sets HTML and we'll do the
    # rest
    HTML = None

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(VulnerableTemplateView, self).dispatch(*args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super(VulnerableTemplateView, self).get_context_data(**kwargs)
        context['title'] = self.title
        context['description'] = self.description
        return context

    def get(self, request, *args, **kwds):
        if self.HTML is not None:
            context = self.get_context_data()
            context['html'] = self.HTML
            return render(request, self.template_name, context)
        else:
            return super(VulnerableTemplateView, self).get(request, *args, **kwds)