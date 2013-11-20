from django.shortcuts import render
from moth.views.base.vulnerable_template_view import VulnerableTemplateView


class StrangeHTTPCodeView(VulnerableTemplateView):
    title = 'Strange HTTP response code detection'
    description = 'Sends a very uncommon HTTP response code'
    url_path = 'strange_http_code.py'

    def get(self, request, *args, **kwds):
        context = self.get_context_data()
        
        status = 527
        context['html'] = 'Error! HTTP response code is 527.'

        return render(request, self.template_name, context, status=status)
