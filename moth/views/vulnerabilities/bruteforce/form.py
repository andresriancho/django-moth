from django.shortcuts import render

from moth.views.base.form_template_view import FormTemplateView
from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit

AUTH_SUCCESS = 'Authentication success, welcome!'
AUTH_ERROR = 'Invalid username and/or password'


class PostLoginForm(forms.Form):
    uname = forms.CharField(label='Username', required=True)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    
    METHOD = 'POST'
    
    def __init__(self, * args, **kwargs):
        # pylint: disable=E1002
        super(PostLoginForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_class = 'form-inline'
        self.helper.form_method = self.METHOD
        
        submit = Submit('Submit', 'Submit', css_class="btn-success")

        self.helper.layout = Layout(
            'uname',
            'password',
            submit,
        )

class GetLoginForm(PostLoginForm):
    METHOD = 'GET'


class PostGuessableCredsLoginFormView(FormTemplateView):
    description = title = 'Guessable credentials in form authentication'
    tags = ['trivial', 'POST']
    url_path = 'guessable_login_form.py'
    users = (('admin', '1234'),)
    form_klass = PostLoginForm
    
    def post(self, request, *args, **kwds):
        context = self.get_context_data()
        
        if (request.POST['uname'], request.POST['password']) in self.users:
            context['message'] = AUTH_SUCCESS
        else:
            context['message'] = AUTH_ERROR
        
        return render(request, self.template_name, context)

class GetGuessableCredsLoginFormView(FormTemplateView):
    description = title = 'Guessable credentials in form authentication'
    tags = ['trivial', 'GET']
    url_path = 'guessable_login_form_get.py'
    users = (('admin', 'admin'),)
    form_klass = GetLoginForm
    
    def get(self, request, *args, **kwargs):
        if 'uname' in request.GET and 'password' in request.GET:
            context = self.get_context_data()
            
            if (request.GET['uname'], request.GET['password']) in self.users:
                context['message'] = AUTH_SUCCESS
            else:
                context['message'] = AUTH_ERROR
                
            return render(request, self.template_name, context)
        
        form = self.form_klass()
        return render(request, self.template_name,
                      self.get_context_data(form=form))

        
        
        
        
