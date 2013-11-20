from django.shortcuts import render
from moth.views.base.vulnerable_template_view import VulnerableTemplateView


class SimpleXSSView(VulnerableTemplateView):
    title = 'Cross-Site scripting (trivial)'
    description = 'Echo query string parameter to HTML without any encoding'
    url_path = 'simple_xss.py?text=1'
    
    def get(self, request, *args, **kwds):
        context = self.get_context_data()
        context['html'] = request.GET['text']
        return render(request, self.template_name, context)
