from django.views.decorators.gzip import gzip_page
from django.shortcuts import render
from django.utils.decorators import method_decorator

from moth.views.base.html_template_view import HTMLTemplateView


class GzipEncodingView(HTMLTemplateView):
    description = title = 'This view uses Gzip to encode the response'
    url_path = 'gzip.html'
    
    @method_decorator(gzip_page)
    def get(self, request, *args, **kwds):
        context = self.get_context_data()
        context['html'] = 'View HTTP response headers.'
        return render(request, self.template_name, context)
