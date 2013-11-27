from django.shortcuts import render
from django import forms
from django.views.decorators.csrf import csrf_exempt

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit

from moth.views.base.vulnerable_template_view import VulnerableTemplateView


class UploadForm(forms.Form):
    _file = forms.FileField()

    def __init__(self, * args, **kwargs):
        super(UploadForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_id = 'upload'
        self.helper.form_action = 'upload.py'
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        
        submit = Submit('Upload', 'Upload', css_class="btn-success")

        # generate layout
        self.helper.layout = Layout(
                                    Field('_file', label='Upload file'),
                                    submit
        )


class ContactView(VulnerableTemplateView):
    template_name = "moth/vulnerability-form.html"
    form_class = UploadForm
    title = description = 'File uploads using multipart'
    url_path = 'upload.py'
    
    def get(self, request, *args, **kwargs):
        """
        Handles GET requests and instantiates a blank version of the form.
        """
        form = UploadForm()
        return render(request, self.template_name,
                      self.get_context_data(form=form))

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance with the passed
        POST variables and then checked for validity.
        """
        has_files = bool(request.FILES)
        msg = 'The file was was successfully uploaded' if has_files else 'Error!'
        
        context = self.get_context_data()
        context['message'] = msg
        
        return render(request, self.template_name, context)
        