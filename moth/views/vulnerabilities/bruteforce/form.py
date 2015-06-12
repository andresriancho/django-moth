from django.shortcuts import render

from moth.views.base.form_template_view import FormTemplateView
from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit

#
#    FIXME: See https://github.com/andresriancho/w3af/issues/799 to understand
#           why we need the * 300
#
AUTH_SUCCESS = 'Authentication success, welcome!' * 300
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


class PasswordOnlyLoginForm(forms.Form):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    
    def __init__(self, * args, **kwargs):
        # pylint: disable=E1002
        super(PasswordOnlyLoginForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_class = 'form-inline'
        
        submit = Submit('Submit', 'Submit', css_class="btn-success")

        self.helper.layout = Layout(
            'password',
            submit,
        )


class PostGuessableCredsLoginFormView(FormTemplateView):
    description = title = 'Guessable credentials in form authentication'
    tags = ['trivial', 'POST']
    url_path = 'guessable_login_form.py'
    users = (('admin', '1234'),)
    form_klass = PostLoginForm
    references = ['https://github.com/andresriancho/w3af/issues/799']
    
    def post(self, request, *args, **kwds):
        context = self.get_context_data()
        
        if (request.POST['uname'], request.POST['password']) in self.users:
            context['message'] = AUTH_SUCCESS
        else:
            context['message'] = AUTH_ERROR
        
        return render(request, self.template_name, context)


class PostImpossibleCredsLoginFormView(PostGuessableCredsLoginFormView):
    description = title = 'Complex credentials in form authentication'
    tags = ['impossible', 'not guessable', 'POST']
    url_path = 'impossible.py'
    users = (('admin', 'admin1ad0min2admin3admi0n4'),)


class PasswordOnlyGuessableCredsLoginFormView(FormTemplateView):
    title = 'Guessable credentials in form authentication'
    description = 'This login form only requires a password'
    tags = ['trivial', 'POST', 'password only']
    url_path = 'guessable_pass_only.py'
    passwords = ('1234',)
    form_klass = PasswordOnlyLoginForm
    references = ['https://github.com/andresriancho/w3af/issues/799']
    
    def post(self, request, *args, **kwds):
        context = self.get_context_data()
        
        if request.POST['password'] in self.passwords:
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
    references = ['https://github.com/andresriancho/w3af/issues/799']
    
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
