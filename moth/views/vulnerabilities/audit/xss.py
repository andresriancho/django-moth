from django.shortcuts import render
from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit

from moth.views.base.vulnerable_template_view import VulnerableTemplateView
from moth.views.base.form_template_view import FormTemplateView


class SimpleXSSView(VulnerableTemplateView):
    title = 'Cross-Site scripting (trivial)'
    description = 'Echo query string parameter to HTML without any encoding'
    url_path = 'simple_xss.py?text=1'
    
    def get(self, request, *args, **kwds):
        context = self.get_context_data()
        context['html'] = request.GET['text']
        return render(request, self.template_name, context)

class XSSForm1(forms.Form):
    text = forms.CharField()
    
    def __init__(self, * args, **kwargs):
        super(XSSForm1, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        submit = Submit('Submit', 'Submit', css_class="btn-success")

        # generate layout
        self.helper.layout = Layout(
                                    Field('text',),
                                    submit
        )
        
class SimpleFormXSSView(FormTemplateView):
    title = 'Cross-Site scripting in form (trivial)'
    description = 'Echo form parameter to HTML without any encoding'
    url_path = 'simple_xss_form.py'
    
    def get(self, request, *args, **kwargs):
        """
        Handles GET requests and instantiates a blank version of the form.
        """
        form = XSSForm1()
        return render(request, self.template_name,
                      self.get_context_data(form=form))
    
    def post(self, request, *args, **kwds):
        context = self.get_context_data()
        context['message'] = request.POST['text']
        return render(request, self.template_name, context)
