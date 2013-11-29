from django.shortcuts import render

from moth.views.base.vulnerable_template_view import VulnerableTemplateView
from moth.views.base.form_template_view import FormTemplateView


class SimpleXSSView(VulnerableTemplateView):
    title = 'Cross-Site scripting'
    tags = ['trivial', 'GET']
    description = 'Echo query string parameter to HTML without any encoding'
    url_path = 'simple_xss.py?text=1'
    
    def get(self, request, *args, **kwds):
        context = self.get_context_data()
        context['html'] = request.GET['text']
        return render(request, self.template_name, context)

class SimpleFormXSSView(FormTemplateView):
    title = 'Cross-Site scripting in form'
    tags = ['trivial', 'POST']
    description = 'Echo form parameter to HTML without any encoding'
    url_path = 'simple_xss_form.py'
    
    def post(self, request, *args, **kwds):
        context = self.get_context_data()
        context['message'] = request.POST['text']
        return render(request, self.template_name, context)
