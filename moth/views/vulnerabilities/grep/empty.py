from django.http import HttpResponse
from moth.views.base.vulnerable_template_view import VulnerableTemplateView


class EmptyResponseView(VulnerableTemplateView):
    title = 'Empty HTTP response body'
    description = 'Empty HTTP response body'
    url_path = 'index.html'

    def get(self, request, *args, **kwds):
        return HttpResponse('')
