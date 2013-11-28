from django.shortcuts import render

from moth.views.base.vulnerable_template_view import VulnerableTemplateView
from moth.forms.generic import GenericForm


class FormTemplateView(VulnerableTemplateView):
    template_name = "moth/vulnerability-form.html"
    form_klass = GenericForm
    
    def get(self, request, *args, **kwargs):
        form = self.form_klass()
        return render(request, self.template_name,
                      self.get_context_data(form=form))
