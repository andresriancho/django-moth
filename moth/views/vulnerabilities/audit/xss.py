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


class FalsePositiveCheck499View(VulnerableTemplateView):
    title = '(almost) Cross-Site Scripting'
    tags = ['false-positive', 'GET', 'filtered']
    description = 'Echo query string parameter to HTML tag attribute removing'\
                  ' the single quotes which are present in the input.'
    url_path = '499_check.py?text=1'
    false_positive_check = True
    references = ['https://github.com/andresriancho/w3af/pull/499']
    
    def get(self, request, *args, **kwds):
        context = self.get_context_data()
        
        text = request.GET['text']
        text = text.replace('"', '')
        
        link = '<a href="http://external/abc/%s">Check link href</a>'
        
        context['html'] = link % text
        
        return render(request, self.template_name, context)

