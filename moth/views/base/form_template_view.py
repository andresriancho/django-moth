from moth.views.base.vulnerable_template_view import VulnerableTemplateView


class FormTemplateView(VulnerableTemplateView):
    template_name = "moth/vulnerability-form.html"
    