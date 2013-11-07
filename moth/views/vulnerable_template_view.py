from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt


class VulnerableTemplateView(TemplateView):
    '''
    All vulnerabilities inherit from this template, which will render the data
    returned by the subclasses, disable anti-CSRF, etc.
    '''
    
    # The template to use to render this view
    template_name = "vulnerability.html"
    
    # The title that will appear on the rendered HTML
    title = None
    
    # The description that will appear on the rendered HTML
    description = None
    
    # The URL pattern (regular expression) which we'll try to match before
    # sending information to this view. This is parsed by the router view.
    url = None

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(VulnerableTemplateView, self).dispatch(*args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super(VulnerableTemplateView, self).get_context_data(**kwargs)
        context['title'] = self.title
        context['description'] = self.description
        return context
